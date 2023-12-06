import logging
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .. import entities, models
from ..database import get_db

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/systems", tags=["System"])


@router.post("", response_model=models.System)
async def create_system(
    request: models.CreateSystem, db: AsyncSession = Depends(get_db)
):
    system = entities.System()
    system.id = uuid4()
    system.name = request.name
    system.supreme_commander = request.supreme_commander
    system.supreme_commander_name: request.supreme_commander_name
    db.add(system)
    await db.commit()

    return system


@router.get("/{system_id}", response_model=models.System)
async def population_sum(system_id: UUID, db: AsyncSession = Depends(get_db)):
    result = (
        select(func.sum(entities.Planet.population_millions))
        .where(entities.Planet.system_id == system_id)
        .group_by(entities.Planet.system_id)
    )
    population_sum = await db.execute(result)

    result = population_sum.scalar()
    if result is None:
        result = 0
    return result
