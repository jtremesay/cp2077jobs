from cp2077jobs.models import JobAdapter
from cp2077jobs.settings import JOBS_FILE

jobs = JobAdapter.validate_json(JOBS_FILE.read_bytes())
for job in jobs:
    print(len(job.quest_givers), job.slug, job.quest_givers)
print(f"Loaded {len(jobs)} jobs from {JOBS_FILE}")
