from functools import cached_property

from loguru import logger


class Torrent(object):
    def __init__(self, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary = dictionary

        for key in self._dictionary.keys():
            if key not in self._keys:
                logger.error(f'Unhandled key in {self.__class__}: {key}: {type(self._dictionary[key])}"{self._dictionary[key]}"')
                continue
            logger.trace(f'{key}: {type(self._dictionary[key])}"{self._dictionary[key]}"')

    @property
    def _keys(self):
        return [
            'filePath',
            'infoHash',
            'format',
            'media',
            'remasterCatalogueNumber',
            'encoding',
            'mb_albumid',
            'id',  # TODO: Create Property
            'remastered',  # TODO: Create Property
            'remasterYear',  # TODO: Create Property
            'remasterTitle',
            'remasterRecordLabel',  # TODO: Create Property
            'scene',  # TODO: Create Property
            'hasLog',  # TODO: Create Property
            'hasCue',  # TODO: Create Property
            'logChecksum',  # TODO: Create Property
            'logCount',  # TODO: Create Property
            'logScore',  # TODO: Create Property
            'fileCount',  # TODO: Create Property
            'size',  # TODO: Create Property
            'seeders',  # TODO: Create Property
            'leechers',  # TODO: Create Property
            'snatched',  # TODO: Create Property
            'freeTorrent',  # TODO: Create Property
            'reported',  # TODO: Create Property
            'time',  # TODO: Create Property
            'description',  # TODO: Create Property
            'fileList',  # TODO: Create Property
            'userId',  # TODO: Create Property
            'username',  # TODO: Create Property
        ]

    def __repr__(self):
        return f'{self.__class__}{self.filePath} ({self.infoHash})'

    def __str__(self):
        return f'{self.filePath} ({self.infoHash})'

    @cached_property
    def infoHash(self):
        return self._dictionary['infoHash']

    @cached_property
    def filePath(self):
        return self._dictionary['filePath']

    @cached_property
    def format(self):
        return self._dictionary['format']

    @cached_property
    def media(self):
        return self._dictionary['media']

    @cached_property
    def mb_albumid(self):
        return self._dictionary.get('mb_albumid', None)

    @cached_property
    def remasterTitle(self):
        return self._dictionary['remasterTitle']

    @cached_property
    def remasterCatalogueNumber(self):
        return self._dictionary['remasterCatalogueNumber']

    @cached_property
    def encoding(self):
        return self._dictionary['encoding'].replace('Lossless', '').replace('24bit', '24').strip()
