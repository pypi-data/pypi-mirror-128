# -*- coding: utf-8 -*-
"""
Represent a string that is absolutely filesystem safe.
"""
from unicodedata import normalize
import transliterate


class SafeString():
    """
    Represent a string that is absolutely filesystem safe.
    """
    whitelist = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                 'y', 'z', '-', ' ', '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9')

    def __init__(self, old_string):
        """Initialize the SafeString object."""
        self.new = str(old_string)

        # Attempt to transliterate non-alphabet scripts:
        try:
            self.new = transliterate.translit(self.new, reversed=True)
        except transliterate.exceptions.LanguageDetectionError:
            pass

        # Apply common cleanup tasks:
        self.new = self.new.lower()
        self.new = self.new.strip()
        normalst = normalize("NFKD", self.new)
        self.new = ''.join(c for c in normalst if ord(c) < 0x7f)
        self.filter()

    def filter(self):
        """Filter out any garbage left.."""
        result = []
        lastWasSpace = False
        for char in self.new:
            for validchar in self.whitelist:
                if char == validchar:

                    # Prevent space duplication.
                    if char == u' ':
                        if lastWasSpace:
                            continue
                        else:
                            lastWasSpace = True
                    else:
                        lastWasSpace = False

                    # Append the character to the result list.
                    result.append(char)
        self.new = ''.join(result).strip()

    def __str__(self):
        """Return the string."""
        return self.new
