from functools import cached_property

from loguru import logger


class Artist(object):
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
            'id',
            'name',
        ]

    def __repr__(self):
        return f'{self.__class__}{self.name} ({self.id})'

    def __str__(self):
        return f'{self.name} ({self.id})'

    @cached_property
    def id(self):
        return self._dictionary['id']

    @cached_property
    def name(self):
        return self._dictionary['name']
