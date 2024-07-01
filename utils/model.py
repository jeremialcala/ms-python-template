# -*- coding: utf-8 -*-
"""
    This util point to create generic objects using json schema.

"""

import jsonschema
from mongoengine import (
    Document,
    StringField,
    UUIDField,
    EmailField,
    ObjectIdField,
    DateTimeField,
    IntField,
    EnumField,
    ImageField
)
from uuid import uuid4
from pydantic import Field, create_model
from bson import ObjectId
from datetime import datetime
from typing import Annotated
from enums import Status
import constants


TYPES = {
        'string': str,
        'array': list,
        'boolean': bool,
        'integer': int,
        'float': float,
        'number': float,
    }


def generate_properties(json_schema: dict) -> dict:
    """
        Using a json file with the document schema
        return a properties for a new dynamic model
    :param json_schema: a plain dict with the schema description
    :return: a dict with all field of the dynamic model
    """
    _model = {}
    for k, v in json_schema.items():
        match v["type"]:
            case constants.UUID_FIELD:
                _model[k] = UUIDField(
                    required=v["required"],
                    unique=v["unique"],
                    default=uuid4()
                )
            case constants.STRING_FIELD:
                _model[k] = StringField(
                    required=v["required"],
                    unique=v["unique"]
                )

            case constants.EMAIL_FIELD:
                _model[k] = EmailField(
                    required=v["required"],
                    unique=v["unique"]
                )

            case constants.DATE_TIME_FIELD:
                _model[k] = DateTimeField(
                    required=v["required"],
                    unique=v["unique"],
                    default=datetime.now()
                )

            case constants.IMAGE_FIELD:
                _model[k] = ImageField(
                    required=v["required"],
                    unique=v["unique"],
                    default=datetime.now()
                )

            case _:
                pass

    _model["createdAt"] = DateTimeField(
        required=False,
        unique=False,
        default=datetime.now()
    )
    _model["status"] = EnumField(
        Status,
        required=True,
        unique=False,
        default=Status.REG
    )
    _model["statusDate"] = DateTimeField(
        required=False,
        unique=False,
        default=datetime.now()
    )

    return _model


def create_dynamic_orm_model(name: str, properties: dict):
    """
        This method will create and return a new dynamic model
    :param name: The name of this model
    :param properties: the scheme definition for this model
    :return: The new dynamic model.
    """
    return type(name, (Document, ), properties)


def create_dynamic_dto_model(name: str, properties: dict):
    """
        this creates a dynamic dto from a json schema.
        { "name": {"type": "String", "description": "this is the description for the field"}}

    :return:
    """
    _model = {}
    for k, v in properties.items():
        _model[k] = Annotated[
            TYPES[v["type"]],
            Field(alias=k, description=v["description"])
        ]

    return create_model(name, **_model)
