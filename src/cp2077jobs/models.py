from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, TypeAdapter

from cp2077jobs.settings import WIKI_BASE_URL


class Game(StrEnum):
    CYBERPUNK_2077 = "Cyberpunk 2077"
    PHANTOM_LIBERTY = "Phantom Liberty"


class JobKind(StrEnum):
    MAIN_JOB = "Main Job"
    SIDE_JOB = "Side Job"
    MINOR_JOB = "Minor Job"
    GIG = "Gig"
    MINOR_ACTIVITY = "Minor Activity"


class MinorActivityKind(StrEnum):
    CYBERPSYCHO_SIGHTING = "Cyberpsycho Sighting"
    INCREASED_CRIMINAL_ACTIVITY = "Increased Criminal Activity"
    REPORTED_CRIME = "Reported Crime"
    SUSPECTED_ORGANIZED_CRIME_ACTIVITY = "Suspected Organized Crime Activity"


class GigKind(StrEnum):
    AGENT_SABOTEUR = "Agent Saboteur"
    GUN_FOR_HIRE = "Gun for Hire"
    SEARCH_AND_RECOVERY = "Search and Recovery"
    SOS_MERC_NEEDED = "SOS: Merc Needed"
    SPECIAL_DELIVERY = "Special Delivery"
    THIEVERY = "Thievery"


class Link(BaseModel):
    slug: str
    name: str

    @property
    def href(self) -> str:
        return WIKI_BASE_URL + self.slug


class Job(BaseModel):
    slug: str
    name: str
    game: Game
    kind: JobKind
    minor_activity_kind: Optional[MinorActivityKind] = None
    gig_kind: Optional[GigKind] = None

    quest_giver: Optional[Link] = None
    districts: list[Link] = Field(default_factory=list)
    sub_districts: list[Link] = Field(default_factory=list)
    locations: list[Link] = Field(default_factory=list)

    xp: Optional[int] = None
    street_cred: Optional[int] = None
    eddies: Optional[int] = None
    items: list[Link] = Field(default_factory=list)

    quests_previous: list[Link] = Field(default_factory=list)
    quests_next: list[Link] = Field(default_factory=list)

    @property
    def href(self) -> str:
        return WIKI_BASE_URL + self.slug


JobAdapter = TypeAdapter(list[Job])
