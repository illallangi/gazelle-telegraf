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
            'year',
            'musicInfo',
            'wikiBody',  # TODO: Create Property
            'bbBody',  # TODO: Create Property
            'wikiImage',  # TODO: Create Property
            'id',  # TODO: Create Property
            'recordLabel',  # TODO: Create Property
            'categoryId',  # TODO: Create Property
            'categoryName',  # TODO: Create Property
            'time',  # TODO: Create Property
            'vanityHouse',  # TODO: Create Property
            'isBookmarked',  # TODO: Create Property
            'tags',  # TODO: Create Property
            'collages',  # TODO: Create Property
            'personalCollages',  # TODO: Create Property
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
        if self.releaseType == 1:
            return 'Album'
        if self.releaseType == 3:
            return 'Soundtrack'
        if self.releaseType == 5:
            return 'EP'
        if self.releaseType == 6:
            return 'Anthology'
        if self.releaseType == 7:
            return 'Compilation'
        if self.releaseType == 9:
            return 'Single'
        if self.releaseType == 11:
            return 'Live album'
        if self.releaseType == 13:
            return 'Remix'
        if self.releaseType == 14:
            return 'Bootleg'
        if self.releaseType == 15:
            return 'Interview'
        if self.releaseType == 16:
            return 'Mixtape'
        if self.releaseType == 17:
            return 'Demo'
        if self.releaseType == 18:
            return 'Concert Recording'
        if self.releaseType == 19:
            return 'DJ Mix'
        if self.releaseType == 21:
            return 'Unknown'
        logger.error(f'Unhandled releaseType in {self}: "{self.releaseType}"')
        return f'Unknown Release Type {self.releaseType}'

    @cached_property
    def year(self):
        return int(self._dictionary['year'])

    @cached_property
    def musicInfo(self):
        return MusicInfo(self._dictionary['musicInfo'])
