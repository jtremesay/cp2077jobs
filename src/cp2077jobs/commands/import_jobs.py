#!/usr/bin/env python3
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Optional

from cp2077jobs.settings import HTML_DIR


class Game(StrEnum):
    CYBERPUNK_2077 = "Cyberpunk 2077"
    PHANTOM_LIBERTY = "Phantom Liberty"


class JobKind(StrEnum):
    MAIN_JOB = "Main Job"
    SIDE_JOB = "Side Job"
    MINOR_JOB = "Minor Job"
    GIG = "Gig"
    MINOR_ACTIVITY = "Minor Activity"


@dataclass
class Job:
    slug: str
    name: str
    game: Game
    kind: JobKind
    quest_giver: Optional[str] = None
    district: Optional[str] = None
    sub_district: Optional[str] = None
    location: Optional[str] = None

    xp: Optional[int] = None
    street_cred: Optional[int] = None
    eddies: Optional[int] = None
    items: list[str] = field(default_factory=list)
    quests_previous: list[str] = field(default_factory=list)
    quests_next: list[str] = field(default_factory=list)


def main():
    # corpo_rat_file = HTML_DIR / "The Corpo-Rat.html"
    # import_job_from_file(corpo_rat)
    # return

    files = sorted(HTML_DIR.glob("*.html"))
