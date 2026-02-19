from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, TypeAdapter


class Game(StrEnum):
    CYBERPUNK_2077 = "Cyberpunk 2077"
    PHANTOM_LIBERTY = "Phantom Liberty"


class JobKind(StrEnum):
    MAIN_JOB = "Main Job"
    SIDE_JOB = "Side Job"
    MINOR_JOB = "Minor Job"
    GIG = "Gig"
    MINOR_ACTIVITY = "Minor Activity"


class Link(BaseModel):
    slug: str
    name: Optional[str] = None


class Job(BaseModel):
    slug: str
    name: str
    game: Game
    kind: JobKind

    quest_givers: list[Link] = Field(default_factory=list)
    districts: list[Link] = Field(default_factory=list)
    sub_districts: list[Link] = Field(default_factory=list)
    locations: list[Link] = Field(default_factory=list)

    xp: Optional[int] = None
    street_cred: Optional[int] = None
    eddies: Optional[int] = None
    items: list[Link] = Field(default_factory=list)

    quests_previous: list[Link] = Field(default_factory=list)
    quests_next: list[Link] = Field(default_factory=list)


Jobs = TypeAdapter(list[Job])
