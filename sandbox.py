from cp2077jobs.models import JobAdapter
from cp2077jobs.settings import JOBS_FILE

jobs = JobAdapter.validate_json(JOBS_FILE.read_bytes())
field = "sub_districts"

for job in jobs:
    value = getattr(job, field)
    print(len(value), job.slug, value)
print(f"Loaded {len(jobs)} jobs from {JOBS_FILE}")
