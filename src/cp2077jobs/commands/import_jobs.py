#!/usr/bin/env python3

from tqdm import tqdm

from cp2077jobs.models import Jobs
from cp2077jobs.settings import BASE_DIR, HTML_DIR


def main():
    jobs_files = BASE_DIR / "jobs.json"
    try:
        jobs = Jobs.validate_json(jobs_files.read_bytes())
    except FileNotFoundError:
        jobs = []
    known_slugs = {job.slug for job in jobs}

    files = sorted(HTML_DIR.glob("*.html"))

    for file in tqdm(files):
        tqdm.write(f"Importing {file.name}")
        if file.stem in known_slugs:
            tqdm.write("Already imported, skipping")
            continue
