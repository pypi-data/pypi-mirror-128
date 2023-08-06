# -*- coding: utf-8 -*-
"""
Represent any file, directory or other reference found on the file system.
"""
import os


class Node():
    """
    Represent any file, directory or other reference found on the file system.

    Hooks:
    - init (obj)
    - remove (obj)
    - move (obj, dest)
    - shell_collect (command)
    """
    dl = 1  # Short for debuglevel.

    def __init__(self, output, path, hooks={}, parent=None, dl=1):
        """Initialize the file-system node object."""
        self.out = output
        self.dl = self.dl + dl
        self.relpath = ''
        self.root = ''
        self.type = self.__class__.__name__
        self.path = os.path.abspath(path)
        self.base = os.path.basename(self.path)
        self.dryrun = False
        self.parent = parent
        self.hooks = hooks

        if parent is None:
            if os.path.isdir(self.path):
                self.root = self.path
            else:
                self.root = os.path.dirname(self.path)
        else:
            self.root = self.parent.root
        self.relpath = self.path.replace('%s/' % self.root, '')

        # Invoke the init hook, see main class description.
        self.invoke('init', self)

    def __str__(self):
        """Format our own base representation."""
        if ' ' in self.base:
            return "'%s'" % self.base
        return self.base

    def invoke(self, hook, *args):
        """Invoke the given hook when they have been registered at object construction."""
        if len(self.hooks) == 0:
            return
        if hook in self.hooks:
            return self.hooks[hook](*args)

    def shellCollect(self, command, *args):
        """Collect the shell equivalent of a file or directory action."""

        # Stop the call if there's no registered hook for this.
        if 'shell_collect' not in self.hooks:
            return

        # Sub function to clean incoming argument values.
        def escape(string):
            string = string.replace('"', '\\"')
            string = string.replace("&", "\&")  # noqa: W605
            string = string.replace('\/', '|')  # noqa: W605
            string = string.replace('`', '\`')  # noqa: W605
            return string

        # Create a new arguments list and escape the values.
        newargs = []
        for a in args:
            newargs.append(escape(a))
        args = tuple(newargs)

        # Parse the command and call our shell_collect hook.
        self.invoke('shell_collect', command.format(*newargs))

    def enableDryRun(self):
        """Enable a dry-run mode on this object so that no real will things happen."""
        self.dryrun = True

    def exists(self):
        """Determine whether the object really exists or not."""
        self.out.log(str(self), '%s.exists' % self.type, self.dl)
        return os.path.exists(self.path)

    def remove(self):
        """Delete the file system object from disk."""
        self.out.log(str(self), '%s.remove' % self.type, self.dl)
        self.shellCollect('rm -v "{}"', self.path)
        if not self.dryrun:
            os.unlink(self.path)

        # Remove this instance from the parents list of children.
        if self.parent is not None:
            self.parent.removeChild(self)

        # Invoke the remove hook, see main class description.
        self.invoke('remove', self)

    def move(self, dest, newFileName=None, onlyReferences=False):
        """Move the file system object onto a different location.."""
        self.out.log(str(self), '%s.move' % self.type, self.dl)

        # Thrown an exception when we're being moved to the same location:
        if id(self) == id(dest):
            raise AssertionError("Can't move '%s' to itself" % dest)

        # Declare the new path and physically move the object.
        self.oldpath = self.path
        if newFileName is not None:
            self.path = os.path.abspath('%s/%s' % (dest.path, newFileName))
        else:
            self.path = os.path.abspath('%s/%s' % (dest.path, self.base))
        if not onlyReferences:
            self.shellCollect('mv -v "{}" "{}"', self.oldpath, self.path)
            if not self.dryrun:
                os.rename(self.oldpath, self.path)

        # Log the move action for retrospection.
        self.out.log("src: '%s'" % self.oldpath.replace(self.root + '/', ''),
                     '%s.move' % self.type, self.dl + 1)
        self.out.log("dst: '%s'" % self.path.replace(self.root + '/', ''),
                     '%s.move' % self.type, self.dl + 1)

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

        # Invoke the move hook, see main class description.
        self.invoke('move', self, dest)
