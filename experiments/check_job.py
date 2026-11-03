"""Log one status check of a queued IBM job to results/ibm-job-status-log.md."""

import datetime as dt
import sys

from entangled_mind import backends, config

LOG = config.RESULTS / "ibm-job-status-log.md"


def main(job_id: str) -> None:
    job = backends.service().job(job_id)
    status = str(job.status())
    ts = job.metrics().get("timestamps", {})
    be = backends.backend()
    now = dt.datetime.now(dt.timezone.utc)
    created = dt.datetime.fromisoformat(ts["created"].replace("Z", "+00:00"))
    if not LOG.exists():
        LOG.write_text("# IBM job status checks\n\n| checked (UTC) | job id | status | waiting (min) | "
                       f"started | finished | `{be.name}` pending jobs |\n|---|---|---|---|---|---|---|\n")
    with LOG.open("a") as f:
        f.write(f"| {now:%Y-%m-%d %H:%M:%S} | `{job_id}` | {status} | {(now - created).total_seconds() / 60:.0f} | "
                f"{ts.get('running') or '—'} | {ts.get('finished') or '—'} | {be.status().pending_jobs} |\n")
    print(status, ts)


if __name__ == "__main__":
    main(sys.argv[1])
