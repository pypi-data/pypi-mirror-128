# -*- coding: utf-8 -*-
"""
Program arguments, defaults and Settings object.
"""
import optparse
import os
import sys
from tagrenamer import __version__
from tagrenamer.app.output import runtime_error


def get_application_context():
    """Define the program's arguments, options and default settings."""
    usage = "usage: %prog [OPTIONS] [DIRECTORY]/"
    version = "%prog {version}".format(version=__version__)
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option(
        "-d", "--dry-run",
        action="store_true", dest="dryrun", default=False,
        help="Perform a dry run and don't touch anything.")
    parser.add_option(
        "-f", "--format",
        action="store", type="string", dest="format", metavar='F',
        default='{artist}/{album}/{artist}-{hash}.{ext}',
        help="The format in which filenames will be rewritten.")
    parser.add_option(
        "-l", "--leftovers",
        action="store", type="string", dest="leftoversdir", metavar='L',
        default='__LEFTOVERS',
        help="The directory where non-music files will be moved to.")
    parser.add_option(
        "-S", "--stagedir",
        action="store", type="string", dest="stagedir", metavar='S',
        default='__STAGE',
        help="Temporary directory before music hits its final spot.")
    parser.add_option(
        "-s", "--shell",
        action="store_true", dest="shell", default=False,
        help="Generate and print shell commands (implies -q and -d)")
    parser.add_option(
        "-q", "--quiet",
        action="store_true", dest="quiet", default=False,
        help="Silence non-debugging output completely.")
    parser.add_option(
        "-v", "--verbose",
        action="count", dest="debuglevel", default=False, metavar='V',
        help="The level of logging verbosity.")
    (options, args) = parser.parse_args()
    return (options, args, parser)


class Settings:
    """
    Settings object.
    """

    def __init__(self):
        """Initialize the Settings object."""
        (options, args, parser) = get_application_context()
        self.options = options
        self.args = args
        self.parser = parser
        self.validate()

    def validate(self):
        """Validate input options and prevent application bugs."""

        if not len(self.args):
            self.parser.print_help()
            sys.exit(0)

        # Store the mandatory directory argument as setting key "dir".
        self.options.dir = str(self.args[0]).strip()

        # Test whether the path exists.
        if not os.path.exists(self.options.dir):
            runtime_error("Directory '%s' not found!" % self.options.dir)

        # Test whether the path is a directory as it should be.
        if not os.path.isdir(self.options.dir):
            runtime_error("Path '%s' not a directory!" % self.options.dir)

        # Enforce dry-run and quiet mode when --shell is passed.
        if self.options.shell:
            self.options.quiet = True
            self.options.dryrun = True

    def __getattr__(self, option):
        """Retrieve options via their name."""
        return self.options.__getattribute__(option)
