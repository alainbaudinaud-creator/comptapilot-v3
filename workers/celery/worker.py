from datetime import datetime
import time


print("CELERY WORKER V3 STARTED")

while True:

    print(
        f"[{datetime.utcnow().isoformat()}] WORKER RUNNING"
    )

    time.sleep(10)
