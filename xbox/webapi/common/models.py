"""Base Models."""
from pydantic import BaseModel

def to_pascal(string):
    return "".join(word.capitalize() for word in string.split("_"))

def to_camel(string):
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])

class PascalCaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_pascal

class CamelCaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel