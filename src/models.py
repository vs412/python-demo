from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PastDatetime,
    validator,
)
from typing import Optional
from .entities import StationType
import re
import http.client
import json


class CreateSystem(BaseModel):
    name: str = Field(strict=True)
    supreme_commander: str
    supreme_commander_name: Optional[str] = None

    @validator("supreme_commander", pre=True, always=True)
    def validate_email(cls, v, values):
        EMAIL_REGIX = re.compile(r"^[a-z0-9]+(?:[._][a-z0-9]+)*@(?:\w+\.)+\w{2,3}$")
        if not EMAIL_REGIX.match(v):
            raise ValueError("Email is not valid")
        return v

    @validator("supreme_commander_name", pre=True, always=True)
    def fetch_supreme_commander_name(cls, v, values):
        url = "users?email=" + values.get("supreme_commander")
        connection = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
        connection.request("GET", url)
        response = connection.getresponse()

        if response.status == 200:
            userdata = json.loads(response.read())
            return userdata[0].get("name")
        else:
            raise ValueError(
                f"user not found with email {values.get('supreme_commander')}"
            )


class System(BaseModel):
    id: UUID
    name: str = Field(strict=True)
    supreme_commander: str
    supreme_commander_name: str
    date_created: PastDatetime


class CreatePlanet(BaseModel):
    name: str = Field(strict=True)
    project_id: UUID
    population_millions: NonNegativeInt = Field(strict=True)
    systen_id: UUID


class UpdatePlanet(BaseModel):
    name: str = Field(strict=True)
    population_millions: NonNegativeInt = Field(strict=True)


class Planet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    project_id: UUID
    population_millions: NonNegativeInt
    systen_id: UUID
    system: System


class CreateStation(BaseModel):
    name: str = Field(strict=True)
    commander: str = Field(strict=True)
    established_on: PastDatetime
    type: StationType
    planet_id: UUID


class UpdateStation(BaseModel):
    name: str = Field(strict=True)
    commander: str = Field(strict=True)
    established_on: PastDatetime
    type: StationType


class Station(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    commander: str
    established_on: PastDatetime
    type: StationType
    planet_id: UUID
    planet: Planet
