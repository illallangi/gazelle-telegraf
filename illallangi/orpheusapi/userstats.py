from functools import cached_property

from bytesize import Size

from loguru import logger


class UserStats(object):
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
            'class',
            'uploaded',
            'downloaded',
            'ratio',
            'requiredratio',
            'bonusPoints',
            'bonusPointsPerHour',
        ]

    @cached_property
    def userclass(self):
        return str(self._dictionary['class'])

    @cached_property
    def uploaded(self):
        return Size(int(self._dictionary['uploaded']))

    @cached_property
    def downloaded(self):
        return Size(int(self._dictionary['downloaded']))

    @cached_property
    def ratio(self):
        return float(self._dictionary['ratio'])

    @cached_property
    def requiredratio(self):
        return float(self._dictionary['requiredratio'])

    @cached_property
    def bonuspoints(self):
        return int(self._dictionary['bonusPoints'])

    @cached_property
    def bonuspointsperhour(self):
        return float(self._dictionary['bonusPointsPerHour'])
