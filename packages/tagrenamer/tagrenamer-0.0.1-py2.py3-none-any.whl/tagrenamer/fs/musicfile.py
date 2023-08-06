# -*- coding: utf-8 -*-
"""
Represent a file of a known music file format found on the file system.
"""
import hashlib
import taglib
from tagrenamer.app.safestring import SafeString
from tagrenamer.fs.file import File


music_extensions = ('mp3', 'MP3', 'ogg', 'OGG', 'flac', 'FLAC')


class MusicFile(File):
    """
    Represent a file of a known music file format found on the file system.

    Hooks:
    - sanitize (obj)
    """

    def __init__(self, output, path, extension, hooks={}, parent=None, dl=1):
        """Initialize the music file object."""
        self.relpath_new = ''
        self.artist = ''
        self.album = ''
        self.title = ''
        self.hash = None
        self.artist_s = ''
        self.album_s = ''
        self.title_s = ''
        self.hash_s = ''
        File.__init__(
            self,
            output,
            path=path,
            extension=extension,
            hooks=hooks,
            parent=parent,
            dl=dl)

        # Set the extension if available.
        self.extension = ''
        if '.' in self.base:
            self.extension = extension

        self.extract()

    def extract(self):
        """Extract all meta data using the Taglib library."""
        self.out.log(str(self), '%s.extract' % self.type, self.dl)
        f = taglib.File(self.path)
        self.artist = ' '.join(f.tags.get('ARTIST', ['unknown_artist']))
        self.album = ' '.join(f.tags.get('ALBUM', ['unknown_album']))
        self.title = ' '.join(f.tags.get('TITLE', ['unknown_title']))
        self.out.log("Artst: '%s'" % self.artist,
                     '%s.extract' % self.type, self.dl + 1)
        self.out.log("Album: '%s'" % self.album,
                     '%s.extract' % self.type, self.dl + 1)
        self.out.log("Title: '%s'" % self.title,
                     '%s.extract' % self.type, self.dl + 1)

    def sanitize(self):
        """Sanitize the extracted data ready for file system level usage."""
        self.out.log(str(self), '%s.sanitize' % self.type, self.dl)
        self.artist_s = str(SafeString(self.artist.strip()))
        self.album_s = str(SafeString(self.album.strip()))
        self.title_s = str(SafeString(self.title.strip()))

        # Start validating the data, based on field length.
        if not len(self.artist_s):
            raise ValueError(self)
        elif not len(self.album_s):
            raise ValueError(self)
        elif not len(self.title_s):
            raise ValueError(self)

        # Generate a hash from all the strings to provide a unique file identifier.
        self.hash = hashlib.md5()
        self.hash.update(self.artist_s.encode('utf-8'))
        self.hash.update(self.album_s.encode('utf-8'))
        self.hash.update(self.title_s.encode('utf-8'))
        self.hash.update(self.extension.encode('utf-8'))
        self.hash_s = str(self.hash.hexdigest())

        # Print the sanitized metadata fields:
        self.out.log("{artist}: '%s'" % self.artist_s,
                     '%s.sanitize' % self.type, self.dl + 1)
        self.out.log("{album}: '%s'" % self.album_s,
                     '%s.sanitize' % self.type, self.dl + 1)
        self.out.log("{title}: '%s'" % self.title_s,
                     '%s.sanitize' % self.type, self.dl + 1)
        self.out.log("{hash}: '%s'" % self.hash_s,
                     '%s.sanitize' % self.type, self.dl + 1)
        self.out.log("{ext}: '%s'" % self.extension,
                     '%s.sanitize' % self.type, self.dl + 1)

        # Invoke the sanitize hook, see main class description.
        self.invoke('sanitize', self)
