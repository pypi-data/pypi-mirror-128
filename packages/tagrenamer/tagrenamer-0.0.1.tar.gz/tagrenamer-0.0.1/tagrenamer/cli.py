# -*- coding: utf-8 -*-
"""
tagrenamer - Mass music collection renamer.
"""
import sys
from tagrenamer.app.output import runtime_error


def main():
    """Main application dispatch routine."""

    try:
        # Import the core libraries and handle import errors:
        try:
            from tagrenamer.app.output import Output
            from tagrenamer.app.settings import Settings
            from tagrenamer.app.collection import Collection
        except ImportError as e:
            runtime_error("%s\n\n"
                          "Check if these Python packages are installed:\n"
                          "- transliterate\n"
                          "- taglib (pytaglib)" % e)

        # Construct the settings and output objects:
        settings = Settings()
        output = Output()
        output.set_debuglevel(settings.debuglevel)
        output.set_quiet(settings.quiet)
        output.log(context=__name__)

        # Dispatch application control to the collection processor.
        collection = Collection(output, settings)
        collection.process()
    except RuntimeError as e:
        print(e)
        return 1
    except KeyboardInterrupt:
        print("Quitting...")
        return -1
    return 0


if __name__ == "__main__":
    sys.exit(main())
