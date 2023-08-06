from enum import Enum

from hardcode_house_model.util.mongo_mixin import MongoMixin
from mongoengine import Document
from mongoengine.fields import (DateTimeField, FloatField, DictField,
                                EmbeddedDocumentField, FloatField, IntField,
                                ListField, StringField, URLField)


class ChangeDirection(Enum):
    Increase = 1
    Decrease = 2
    Newlisting = 3
    Delisting = 4
