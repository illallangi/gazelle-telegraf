from functools import cached_property

from loguru import logger

from .artistcollection import ArtistCollection


class MusicInfo(object):
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
            'artists',
            'with',
            'remixedBy',
            'composers',
            'conductor',
            'dj',
            'producer',
        ]

    def __repr__(self):
        return f'{self.__class__}{self.name}'

    def __str__(self):
        return f'{self.name}'

    @cached_property
    def artists(self):
        return ArtistCollection(self._dictionary['artists'])

    @cached_property
    def withArtists(self):
        return ArtistCollection(self._dictionary['with'])

    @cached_property
    def remixedBy(self):
        return ArtistCollection(self._dictionary['remixedBy'])

    @cached_property
    def composers(self):
        return ArtistCollection(self._dictionary['composers'])

    @cached_property
    def conductors(self):
        return ArtistCollection(self._dictionary['conductor'])

    @cached_property
    def djs(self):
        return ArtistCollection(self._dictionary['dj'])

    @cached_property
    def producers(self):
        return ArtistCollection(self._dictionary['producer'])
