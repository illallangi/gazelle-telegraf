from functools import cached_property

from loguru import logger

from .musicinfo import MusicInfo


class Group(object):
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
            'name',
            'catalogueNumber',
            'releaseType',
            'releaseTypeName',
            'year',
            'musicInfo',
            'wikiBody',  # TODO: Create Property
            'wikiBBcode',  # TODO: Create Property
            'wikiImage',  # TODO: Create Property
            'id',  # TODO: Create Property
            'recordLabel',  # TODO: Create Property
            'categoryId',  # TODO: Create Property
            'categoryName',  # TODO: Create Property
            'time',  # TODO: Create Property
            'vanityHouse',  # TODO: Create Property
            'isBookmarked',  # TODO: Create Property
            'tags',  # TODO: Create Property
        ]

    def __repr__(self):
        return f'{self.__class__}{self.name}'

    def __str__(self):
        return f'{self.name}'

    @cached_property
    def name(self):
        return self._dictionary['name']

    @cached_property
    def catalogueNumber(self):
        return self._dictionary['catalogueNumber']

    @cached_property
    def releaseType(self):
        return int(self._dictionary['releaseType'])

    @cached_property
    def releaseTypeName(self):
        return self._dictionary['releaseTypeName']

    @cached_property
    def year(self):
        return int(self._dictionary['year'])

    @cached_property
    def musicInfo(self):
        return MusicInfo(self._dictionary['musicInfo'])
