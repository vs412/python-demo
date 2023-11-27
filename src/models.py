from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PastDatetime

from .entities import StationType


class CreatePlanet(BaseModel):
    name: str = Field(strict=True)
    project_id: UUID
    population_millions: NonNegativeInt = Field(strict=True)


class UpdatePlanet(BaseModel):
    name: str = Field(strict=True)
    population_millions: NonNegativeInt = Field(strict=True)


class Planet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    project_id: UUID
    population_millions: NonNegativeInt


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
