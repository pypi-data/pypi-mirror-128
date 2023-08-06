# -*- coding: utf-8 -*-
"""
Represent the collection of all found file objects within the base path.
"""
import os
import hashlib
from tagrenamer import __version__
from tagrenamer.fs.directory import Directory
from tagrenamer.app.output import runtime_error


class Collection():
    """
    Represent the collection of all found file objects within the base path.
    """

    def __init__(self, output, settings):
        """Initialize the collection."""
        self.settings = settings
        self.out = output

        self.d_leftovers = None
        self.d_root = None
        self.d_stage = None
        self.directories = []
        self.files = []
        self.hashes = []
        self.ids = []
        self.musicfiles = []
        self.musicfiles_new_relpaths = []
        self.type = self.__class__.__name__
        self.nodes = []

        self.out.log(
            context='%s.__init__' % self.type, level=1)

        # Initialize all directory objects: the root directory,
        # the left-overs and stage directories.
        self.d_root = Directory(
            output=self.out,
            path=self.settings.dir,
            hooks={
                'init': self.callbackInit,
                'remove': self.callbackRemove,
                'move': self.callbackMove,
                'sanitize': self.callbackSanitize,
                'traverse_filter': self.callbackTraverseFilter,
                'shell_collect': self.callbackShellCollect,
                'mkdir': self.callbackMkdir})
        self.d_leftovers = Directory(
            output=self.out,
            path="%s/%s" % (self.d_root.path, self.settings.leftoversdir),
            hooks={'shell_collect': self.callbackShellCollect},
            dl=2)
        self.d_stage = Directory(
            output=self.out,
            path="%s/%s" % (self.d_root.path, self.settings.stagedir),
            hooks={'shell_collect': self.callbackShellCollect},
            parent=self.d_root,
            dl=2)

        # If we run in --dry-run mode, enable it on all directory objects.
        if self.settings.dryrun:
            self.d_root.enableDryRun()
            self.d_leftovers.enableDryRun()
            self.d_stage.enableDryRun()

    def process(self):
        """Process the collection."""
        self.out.write(" - Tagrenamer version %s." % __version__)
        self.initializeDirectories()
        self.traverse()
        self.sanitize()
        self.moveLeftovers()
        self.moveMusicToStage()
        self.removeEmptyDirectories()
        self.moveFilesPermanently()
        self.removeStageDirectory()
        self.removeLeftoversDirectory()
        self.finish()

    def __str__(self):
        """Format our own base representation."""
        return self.settings.dir.rstrip('/')

    def initializeDirectories(self):
        """Initialize the leftovers and staging directories."""
        self.out.log(
            context='%s.initializeDirectories' % self.type, level=1)
        # LEFTOVERS DIRECTORY: Clean the directory or create it.
        if self.d_leftovers.exists():
            self.d_leftovers.traverse()
            if len(self.d_leftovers.children):
                for c in self.d_leftovers.children:
                    c.remove()
            self.out.write(
                " - Leftovers directory '%s/' cleaned."
                % self.settings.leftoversdir)
        else:
            self.d_leftovers.mkdir()
            self.out.write(
                " - Leftovers directory '%s/' created."
                % self.settings.leftoversdir)

        # STAGE DIRECTORY: Create the directory or verify it is empty when it exists.
        if self.d_stage.exists():
            self.d_stage.traverse()
            if len(self.d_stage.children) != 0:
                runtime_error(
                    "Stage directory '%s/' exist but is NOT empty!"
                    % self.settings.stagedir)
            else:
                self.out.write(
                    " - Stage directory '%s/' exists."
                    % self.settings.stagedir)
        else:
            self.d_stage.mkdir()
            self.out.write(
                " - Stage directory '%s/' created." % self.settings.stagedir)

    def traverse(self):
        """Traverse the base path where the music resides in and pass our registrar."""
        self.out.log(
            context='%s.traverse' % self.type, level=1)
        self.out.write(" - Traverse the collection and extract music tags.")
        self.d_root.traverse()

    def sanitize(self):
        """Sanitize all extracted meta data for file system usage and validate input."""
        self.out.log(
            context='%s.sanitize' % self.type, level=1)
        self.out.write(" - Validating tag input and sanitizing variables.")
        for f in self.musicfiles:
            try:
                f.sanitize()
            except ValueError:
                runtime_error(
                    "Please correct the tags of this file:\n%s" % f.path)

    def moveLeftovers(self):
        """Move all the non-music files into the leftovers directory.."""
        self.out.log(
            context='%s.moveLeftovers' % self.type, level=1)
        self.out.write(
            " - Moving non music files to '%s/'." % self.settings.leftoversdir)

        # Iterate the files - which ain't music - and relocate them to the left-overs
        # directory while recreating the original directory structure. After this our
        # self.files index will be empty as they're disregarded from our index.
        for f in self.files:
            if os.path.dirname(f.relpath) != '':
                destination = self.d_leftovers.mkdirs(os.path.dirname(f.relpath))
            else:
                destination = self.d_leftovers
            f.move(destination)

    def moveMusicToStage(self):
        """Rename the music files and move them into the new structure (inside stage)."""
        self.out.log(
            context='%s.moveMusicToStage' % self.type, level=1)
        self.out.write(
            " - Moving music to new tree in stage directory '%s/'."
            % self.settings.stagedir)
        for f in self.musicfiles:
            destination_dir = os.path.dirname(f.relpath_new)
            if destination_dir == '':
                destination_dir = self.d_stage
            else:
                destination_dir = self.d_stage.mkdirs(destination_dir)
            f.move(destination_dir, os.path.basename(f.relpath_new))

    def removeEmptyDirectories(self):
        """Remove empty directories in the main music tree."""
        self.out.log(
            context='%s.removeEmptyDirectories' % self.type, level=1)
        self.out.write(
            " - Remove empty directories (except stage/leftover directories).")
        for c in self.d_root.children:
            if c.type == 'Directory':
                c.remove()

    def moveFilesPermanently(self):
        """Move all files and directories from stage to the permanent spot."""
        self.out.log(
            context='%s.moveFilesPermanently' % self.type, level=1)
        self.out.write(
            " - Move everything from stage into the final location.")
        for c in self.d_stage.children:
            c.move(self.d_root)

    def removeStageDirectory(self):
        """Remove the stage directory and object."""
        self.out.log(
            context='%s.removeStageDirectory' % self.type, level=1)
        self.out.write(
            " - Deleting the temporary stage directory '%s/'."
            % self.settings.stagedir)
        self.d_stage.remove()
        del self.d_stage
        self.d_stage = None

    def removeLeftoversDirectory(self):
        """Remove the left-overs directory and object."""
        self.out.log(
            context='%s.removeLeftoversDirectory' % self.type, level=1)
        if len(self.d_leftovers.children) == 0:
            self.out.write(
                " - Deleting the empty leftovers directory '%s/'."
                % self.settings.leftoversdir)
            self.d_leftovers.remove()
            del self.d_leftovers
            self.d_leftovers = None

    def finish(self):
        """Cleanup and drop some statistics."""
        self.out.log(
            context='%s.finish' % self.type, level=1)
        if self.settings.dryrun:
            self.out.write(
                " - DONE! Processed %d files (dry-run mode)."
                % len(self.musicfiles))
        else:
            self.out.write(
                " - DONE! Processed %d files." % len(self.musicfiles))

    # HOOK IMPLEMENTATIONS #####################################################

    def callbackInit(self, node):
        """Register a reference to any new created file system node in this collection."""
        if id(node) in self.ids:
            return
        self.ids.append(id(node))
        if node.type == 'Directory':
            self.directories.append(node)
        elif node.type == 'File':
            self.files.append(node)
        elif node.type == 'MusicFile':
            self.musicfiles.append(node)
        else:
            self.nodes.append(node)

    def callbackRemove(self, node):
        """Implementation of the remove hook - remove the object from our music index."""

        # Rewrite the ids list - without the given node.
        ids = []
        for i in self.ids:
            if i != id(node):
                ids.append(i)
        self.ids = ids

        # Rewrite any of the trees to forget the object.
        index = []
        if node.type == 'Directory':
            for d in self.directories:
                if id(d) != id(node):
                    index.append(d)
            self.directories = index
        elif node.type == 'File':
            for f in self.files:
                if id(f) != id(node):
                    index.append(f)
            self.files = index
        elif node.type == 'MusicFile':
            for f in self.musicfiles:
                if id(f) != id(node):
                    index.append(f)
            self.musicfiles = index
        else:
            for n in self.nodes:
                if id(n) != id(node):
                    index.append(n)
            self.nodes = index

        # In case of a MusicFile, lets also rewrite the hash and relpath's registry.
        if node.type == 'MusicFile':
            musicfiles_new_relpaths = []
            hashes = []
            for h in self.hashes:
                if h != node.hash_s:
                    hashes.append(h)
            for mnr in self.musicfiles_new_relpaths:
                if mnr != node.relpath_new:
                    musicfiles_new_relpaths.append(mnr)
            self.hashes = hashes
            self.musicfiles_new_relpaths = musicfiles_new_relpaths

    def callbackMove(self, node, dest):
        """Implementation of the move hook."""

        # Detect if the object being moved - for instance a left over file - goes
        # outside of our index, and forget about it if it does.
        if self.callbackMoveIsDestinationUnknown(dest):
            self.callbackRemove(node)

    def callbackMoveIsDestinationUnknown(self, dest):
        """Test if the destination or any parents aren't in our collection."""
        if id(dest) in self.ids:
            return False
        else:
            if dest.parent is not None:
                return self.callbackMoveIsDestinationUnknown(dest.parent)
            else:
                return True

    def callbackSanitize(self, node):
        """Implementation of the sanitize hook."""

        # Define a callable to generate a file based hash.
        def md5(filename, block_size=2**20):
            f = open(filename)
            md5 = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
            return md5.hexdigest()

        # Verify if a song with exactly the same artist, album, title wasn't
        # submitted before and abort the process if it does.
        if node.hash_s in self.hashes:
            self.out.write("\nERROR: the following file has been identified as a duplicate!\n")
            self.out.write("What this means is that we scanned a file earlier with exactly the")
            self.out.write("same artist, album, title and extension. To prevent this from")
            self.out.write("causing any conflicts we need you to sort this out first.\n")
            self.out.write("File:   '%s'" % node.relpath)
            self.out.write("Artist: '%s'" % node.artist)
            self.out.write("Album:  '%s'" % node.album)
            self.out.write("Title:  '%s'" % node.title)
            runtime_error("Aborted, no files have been touched!")
        else:
            self.hashes.append(node.hash_s)

        # Create a dictionary with replaceable strings, our formatting arguments.
        kwarguments = {
            'artist': node.artist_s,
            'album': node.album_s,
            'title': node.title_s,
            'hash': node.hash_s,
            'ext': node.extension.lower()}

        # Parse the format and set the relpath_new field to reflect the new location.
        try:
            node.relpath_new = self.settings.format.format(**kwarguments)
        except KeyError:
            runtime_error("The provided format contains invalid fields:\n%s"
                          % self.settings.format)

        # Verify if a different file with exactly the same relpath_new isn't staged:
        if node.relpath_new in self.musicfiles_new_relpaths:
            runtime_error("The following file appears to be a duplicate!\n\n"
                          "File:     '%s'\n"
                          "New path: '%s'\n"
                          "Artist:   '%s'\n"
                          "Album:    '%s'\n"
                          "Title:    '%s'\n"
                          % (node.relpath,
                             node.relpath_new,
                             node.artist,
                             node.album,
                             node.title))
        else:
            self.musicfiles_new_relpaths.append(node.relpath_new)

    def callbackTraverseFilter(self, node, path):
        """Implementation of the traverse_filter hook."""

        # Skip including the leftovers and stage directories within the music tree.
        if path == self.d_leftovers.path:
            return False
        if path == self.d_stage.path:
            return False
        return True

    def callbackShellCollect(self, command):
        """Implementation of the shell_collect hook."""
        if self.settings.shell:
            print(command)

    def callbackMkdir(self, node):
        """Implementation of the mkdir hook."""
        pass
