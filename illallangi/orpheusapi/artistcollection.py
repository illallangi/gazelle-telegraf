from collections.abc import Sequence

from .artist import Artist


class ArtistCollection(Sequence):
    def __init__(self, sequence, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sequence = [Artist(t) for t in sequence]

    def __repr__(self):
        return f'{self.__class__}()[{self.__len__()}]'

    def __str__(self):
        return f'{self.__len__()} Artist{"" if self.__len__() == 1 else "s"}'

    def __iter__(self):
        return self._sequence.__iter__()

    def __getitem__(self, key):
        return self._sequence.__getitem__(key)

    def __len__(self):
        return self._sequence.__len__()
