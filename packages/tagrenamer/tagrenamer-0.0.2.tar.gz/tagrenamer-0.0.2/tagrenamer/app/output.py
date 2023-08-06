# -*- coding: utf-8 -*-
"""
Combined output and logging facility with level support.
"""
from datetime import datetime


def runtime_error(message):
    """Stop the program using a prefixed RuntimeError."""
    output = Output()
    output.runtime_error(message)


class Output:
    """
    Combined output and logging facility with level support.
    """

    def __init__(self):
        """Initialize the logger."""
        self.debuglevel = False
        self.quiet = False

    def set_debuglevel(self, level):
        """Set the level of debugging."""
        self.debuglevel = level

    def set_quiet(self, quiet):
        """Enable or disable quiet mode."""
        self.quiet = quiet

    def runtime_error(self, message):
        """Stop the program using a prefixed RuntimeError."""
        error = ['']
        for line in message.split("\n"):
            error.append('ERROR: ' + line)
        error.append('')
        raise RuntimeError("\n".join(error))

    def log(self, message='', context='', level=0):
        """Log a string at the given indentation level."""
        if not self.debuglevel:
            return

        # Skip messages with a higher debuglevel level.
        if level+1 > self.debuglevel:
            return

        # Generate the indentation spacing.
        indent = []
        level = (level * 4) + 2
        for x in range(0, level):
            indent.append(' ')

        # Generate the prefix string.
        now = datetime.now()
        prefix = []
        prefix.append('%s  ' % now.strftime('%H:%M:%S'))
        if context:
            context = '<%s>  ' % context
            prefix.append(context.ljust(5))
        prefix.append(''.join(indent))
        prefix = ''.join(prefix)

        # Delegate output writing to write():
        if message:
            for line in message.split("\n"):
                print(prefix + line)
        else:
            print(prefix)

    def write(self, message):
        """Print the given message when not-quiet."""
        if self.quiet:
            return
        print(message)
