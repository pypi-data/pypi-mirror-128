# -*- coding: utf-8 -*-
"""
Represent a directory found on the file system.
"""
import os
from tagrenamer.fs.node import Node
from tagrenamer.fs.file import File
from tagrenamer.fs.musicfile import MusicFile, music_extensions


class Directory(Node):
    """
    Represent a directory found on the file system.

    Hooks:
    - traverse_filter (obj, path), return True/False
    - mkdir (obj)
    """

    def __init__(self, output, path, hooks={}, parent=None, dl=1):
        """Initialize the directory object."""
        self.children = []
        Node.__init__(
            self,
            output,
            path=path,
            hooks=hooks,
            parent=parent,
            dl=dl)

    def enableDryRun(self):
        """Enable a dry-run mode on this object and its children.."""
        Node.enableDryRun(self)
        if len(self.children):
            for c in self.children:
                c.enableDryRun()

    def addChild(self, child):
        """Add a child node."""
        children = []
        for c in self.children:
            children.append(c)
        children.append(child)
        self.children = children

    def removeChild(self, child):
        """Remove a child from this node."""
        children = []
        for c in self.children:
            if c.path != child.path:
                children.append(c)
        self.children = children

    def traverse(self):
        """Traverse into subdirectories and load our children."""
        self.children = []
        self.out.log(str(self), '%s.traverse' % self.type, self.dl)

        # Only really traverse if the object exists.
        if self.exists():
            for path in os.listdir(self.path):
                dl = self.dl + 1
                path = "%s/%s" % (self.path, path)

                # Invoke the traverse_filter hook (see main class description) and
                # determine if we should include this object (True) or not (False).
                filter_outcome = self.invoke('traverse_filter', self, path)
                if filter_outcome is not None:
                    if filter_outcome is False:
                        self.out.log('%s (skipping)' % str(self),
                                     '%s.traverse' % self.type,
                                     self.dl)
                        continue

                # Perform a set of tests and load the correct class for the found child.
                if os.path.isdir(path):
                    node = Directory(output=self.out,
                                     path=path,
                                     hooks=self.hooks,
                                     parent=self,
                                     dl=dl)
                    node.traverse()
                elif os.path.isfile(path):
                    extension = path.split('.').pop()
                    if extension in music_extensions:
                        node = MusicFile(output=self.out,
                                         path=path,
                                         extension=extension,
                                         hooks=self.hooks,
                                         parent=self,
                                         dl=dl)
                    else:
                        node = File(output=self.out,
                                    path=path,
                                    extension=extension,
                                    hooks=self.hooks,
                                    parent=self,
                                    dl=dl)
                else:
                    node = Node(output=self.out,
                                path=path,
                                hooks=self.hooks,
                                parent=self,
                                dl=dl)

                # Enable dry run if on the node if it applies to us.
                if self.dryrun:
                    node.enableDryRun()

                # Append the child to our list of children.
                self.children.append(node)

    def mkdir(self):
        """Make this directory if it doesn't exist on disk yet."""
        self.out.log(str(self), '%s.mkdir' % self.type, self.dl)
        if not self.dryrun:
            os.mkdir(self.path)
        self.shellCollect('mkdir -v "{}"', self.path)

        # Invoke the mkdir hook, see main class description.
        self.invoke('mkdir', self)

    def mkdirs(self, path):
        """Make multiple directories at once and assure that a path exists."""
        self.out.log(context='%s.mkdirs' % self.type, level=self.dl)

        # Calculate the sub path and current base being looked for.
        path = path.split('/')
        base = path[0]
        del path[0]

        # Determine whether the top level of the trail already exists.
        existingDir = False
        for c in self.children:
            if c.base == base:
                existingDir = c

        # Load the new directory object and create it if needed.
        if not existingDir:
            dl = self.dl + 1
            npath = "%s/%s" % (self.path, base)
            dir = Directory(output=self.out,
                            path=npath,
                            hooks=self.hooks,
                            parent=self,
                            dl=dl)
            if self.dryrun:
                dir.enableDryRun()
            dir.mkdir()
            self.children.append(dir)
        else:
            dir = existingDir

        # Let the fresh directory object recurse into itself.
        if len(path):
            return dir.mkdirs('/'.join(path))
        return dir

    def remove(self):
        """Delete this directory and it's siblings from disk."""
        self.out.log(str(self), '%s.remove' % self.type, self.dl)

        # Start with removing my children and their references.
        for c in self.children:
            c.remove()
        self.children = []

        # Remove the directory when it's emptied.
        self.shellCollect('rm -Rv "{}"', self.path)
        if not self.dryrun:
            os.rmdir(self.path)

        # Remove this instance from the parents list of children.
        if self.parent is not None:
            self.parent.removeChild(self)

        # Invoke the remove hook, see main class description.
        self.invoke('remove', self)

    def move(self, dest, onlyReferences=False):
        """Move the file system object onto a different location."""
        self.out.log(str(self), '%s.move' % self.type, self.dl)

        # Thrown an exception when we're being moved to the same location:
        if id(self) == id(dest):
            raise AssertionError("Can't move '%s' to itself" % dest)

        # Declare the new path and physically move the object.
        self.oldpath = self.path
        self.path = os.path.abspath('%s/%s' % (dest.path, self.base))
        if not onlyReferences:
            self.shellCollect('mv -v "{}" "{}"', self.oldpath, self.path)
            if not self.dryrun:
                os.rename(self.oldpath, self.path)

        # Unregister ourselves at our current parent and register at new parent.
        if self.parent:
            self.parent.removeChild(self)
            dest.addChild(self)

        # Re-parent ourselves and update several properties.
        self.parent = dest
        self.base = os.path.basename(self.path)
        self.dryrun = self.parent.dryrun
        self.root = self.parent.root
        self.relpath = self.path.replace('%s/' % self.root, '')
        self.dl = self.parent.dl + 1

        # Iterate our children and ensure they're moved too.
        for c in self.children:
            c.move(dest=self, onlyReferences=True)

        # Invoke the move hook, see main class description.
        self.invoke('move', self, dest)
