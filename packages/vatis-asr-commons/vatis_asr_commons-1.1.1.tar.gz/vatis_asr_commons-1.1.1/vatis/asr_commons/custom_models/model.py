import uuid
from enum import Enum

from vatis.asr_commons.config import Language


class Model:
    def __init__(self, uid, language: Language, name: str, description: str = ''):
        assert uid is not None
        assert language is not None
        assert name is not None

        if isinstance(uid, str):
            self._uid = uuid.UUID(uid)
        elif isinstance(uid, uuid.UUID):
            self._uid = uid
        else:
            raise ValueError('Unsupported type: ' + str(type(uid)))

        self._language = language
        self._name = name
        self._description = description

    @property
    def uid(self) -> uuid.UUID:
        return self._uid

    @property
    def language(self) -> Language:
        return self._language

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def __str__(self):
        return f'{str(self._uid)} {self._name} {str(self._language)}'

    def __eq__(self, other):
        if not isinstance(other, Model):
            return NotImplemented

        return self._uid == other._uid

    def __hash__(self):
        return hash(self._uid)


class ModelType(Enum):
    ACOUSTIC: str = 'AM'
    LINGUISTIC: str = 'LM'
