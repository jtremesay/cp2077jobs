#!/usr/bin/env python3

import logfire
from pydantic_ai import Agent
from pydantic_ai.messages import BinaryContent
from tqdm import tqdm

from cp2077jobs.models import Job, Jobs
from cp2077jobs.settings import BASE_DIR, HTML_DIR, MODEL_NAME

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic_ai()

system_prompt = f"""
You are a helpful assistant for extracting structured data about jobs in the game Cyberpunk 2077 from HTML pages. 
You will be given the HTML content of a page describing a job, and you need to extract the relevant information and return it in a structured format.

A job has the followoing structure :
``°`json
{Job.model_json_schema()}
```

Use the steam as slug (`(Don%27t_Fear)_The_Reaper.html` or `https://cyberpunk.fandom.com/wiki/(Don%27t_Fear)_The_Reaper` -> `(Don%27t_Fear)_The_Reaper`).
The HTML content may contain various sections such as the job's name, quest giver, location, rewards, and prerequisites.
Extract as much information as possible from the HTML content and populate the fields of the Job model accordingly. If certain information is not available in the HTML, you can leave the corresponding fields as null or empty.
Extract only meaningful things, mostly the one that have a link in the wiki page (quest giver, location, items, quests previous and next). For example, if the quest giver is a named character with a wiki page, extract it as a Link with the name and slug. If it's just a generic character without a wiki page, you can ignore it.
"""

agent = Agent(
    model=MODEL_NAME,
    system_prompt=system_prompt,
    output_type=Job,
    retries=10,
)


def main():
    # corpo_rat_file = HTML_DIR / "The Corpo-Rat.html"
    # import_job_from_file(corpo_rat)
    # return
    # print(system_prompt)
    # return

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

        r = agent.run_sync(
            [
                f"Import the job from the following HTML file: {file.name}",
                BinaryContent(
                    data=file.read_bytes(),
                    media_type="text/plain",
                    identifier=str(file),
                ),
            ]
        )
        tqdm.write(f"Output: {r.output}")
        jobs.append(r.output)

        (BASE_DIR / "jobs.json").write_bytes(Jobs.dump_json(jobs, indent=2))
        known_slugs.add(file.stem)
