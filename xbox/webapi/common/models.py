"""Base Models."""
from pydantic import BaseModel


def to_pascal(string):
    return "".join(word.capitalize() for word in string.split("_"))


def to_camel(string):
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def to_lower(string):
    return string.replace("_", "")


class PascalCaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = to_pascal


class CamelCaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = to_camel


class LowerCaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        alias_generator = to_lower
