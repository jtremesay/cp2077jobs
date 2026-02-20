#!/usr/bin/env python3

from itertools import pairwise
from typing import Optional

from bs4 import BeautifulSoup, Tag
from tqdm import tqdm

from cp2077jobs.models import (
    Game,
    GigKind,
    Job,
    JobAdapter,
    JobKind,
    Link,
    MinorActivityKind,
)
from cp2077jobs.settings import HTML_DIR, JOBS_FILE


class JobBuilder:
    def __init__(self) -> None:
        self.slug: Optional[str] = None
        self.name: Optional[str] = None
        self.game: Optional[Game] = None
        self.kind: Optional[JobKind] = None
        self.minor_activity_kind: Optional[MinorActivityKind] = None
        self.gig_kind: Optional[GigKind] = None

        self.quest_giver: Optional[Link] = None
        self.district: Optional[Link] = None
        self.sub_districts = []
        self.locations = []

        self.xp = None
        self.street_cred = None
        self.eddies = None

        self.items = []

        self.quests_previous = []
        self.quests_next = []

    def build(self) -> Job:
        return Job(
            slug=self.slug,
            name=self.name,
            game=self.game,
            kind=self.kind,
            minor_activity_kind=self.minor_activity_kind,
            gig_kind=self.gig_kind,
            quest_giver=self.quest_giver,
            district=self.district,
            sub_districts=self.sub_districts,
            locations=self.locations,
            xp=self.xp,
            street_cred=self.street_cred,
            eddies=self.eddies,
            items=self.items,
            quests_previous=self.quests_previous,
            quests_next=self.quests_next,
        )


def extract_from_aside(builder: JobBuilder, aside_node: Tag) -> None:
    builder.name = aside_node.select_one("h2").text.strip()

    for section_node in aside_node.select("section.pi-group"):
        title_node = section_node.select_one("h2")
        if title_node is None:
            continue

        title = title_node.text.strip()
        match title:
            case "General":
                for row_node in section_node.select("div.pi-item"):
                    key = row_node.select_one("h3").text.strip()
                    match key:
                        case "Type":
                            job_kind_name = row_node.select_one(
                                "div.pi-data-value"
                            ).text.strip()
                            try:
                                builder.kind = JobKind(job_kind_name)
                            except ValueError:
                                try:
                                    builder.minor_activity_kind = MinorActivityKind(
                                        job_kind_name
                                    )
                                except ValueError:
                                    try:
                                        builder.gig_kind = GigKind(job_kind_name)
                                    except ValueError:
                                        raise ValueError(
                                            f"Unknown job kind: {job_kind_name}"
                                        )
                                    else:
                                        builder.kind = JobKind.GIG
                                else:
                                    builder.kind = JobKind.MINOR_ACTIVITY

                        case "Quest Giver":
                            if link_node := row_node.select_one("div.pi-data-value a"):
                                builder.quest_giver = Link(
                                    slug=link_node["href"].rsplit("/", 1)[-1],
                                    name=link_node.text.strip(),
                                )

                        case "District":
                            if link_node := row_node.select_one("div.pi-data-value a"):
                                builder.district = Link(
                                    slug=link_node["href"].rsplit("/", 1)[-1],
                                    name=link_node.text.strip(),
                                )

            case "Additional":
                pass

            case "Rewards":
                pass

            case "Quest Chain":
                pass

            case _:
                raise ValueError(f"Unknown section title: {title}")


def search_job_kind_in_category_nodes(
    builder: JobBuilder, category_nodes: list[Tag]
) -> None:
    for category_node in category_nodes:
        category_name = category_node.text.strip()
        match category_name:
            case "Cyberpunk 2077 Main Jobs":
                builder.kind = JobKind.MAIN_JOB

            case "Cyberpunk 2077 Side Jobs":
                builder.kind = JobKind.SIDE_JOB

            case "Cyberpunk 2077 Minor Jobs":
                builder.kind = JobKind.MINOR_JOB

            case "Cyberpunk 2077 Gigs":
                builder.kind = JobKind.GIG

            case "Cyberpunk 2077 Minor Activities":
                builder.kind = JobKind.MINOR_ACTIVITY


def search_game_in_soup(builder: JobBuilder, soup: BeautifulSoup):
    for t1, t2 in pairwise(map(lambda x: x.text.strip(), soup.select("a"))):
        if t1 == "Cyberpunk 2077" and t2 == "Phantom Liberty":
            print("Found both Cyberpunk 2077 and Phantom Liberty links")
            builder.game = Game.PHANTOM_LIBERTY
            return

    builder.game = Game.CYBERPUNK_2077


def import_job_from_soup(builder: JobBuilder, soup: BeautifulSoup) -> Job:
    aside_node = soup.find("aside")
    extract_from_aside(builder, aside_node)

    if builder.kind is None:
        search_job_kind_in_category_nodes(
            builder, soup.select(".page-header__categories a")
        )

    search_game_in_soup(builder, soup)

    return builder.build()


def import_job_from_file(file) -> Job:
    builder = JobBuilder()
    builder.slug = file.stem
    soup = BeautifulSoup(file.read_text(), "lxml")
    return import_job_from_soup(builder, soup)


def main():
    files = sorted(HTML_DIR.glob("*.html"))

    jobs = []
    for file in tqdm(files):
        tqdm.write(f"Importing https://cyberpunk.fandom.com/wiki/{file.stem}")
        job = import_job_from_file(file)
        if job is not None:
            jobs.append(job)
            JOBS_FILE.write_bytes(JobAdapter.dump_json(jobs, indent=2))
