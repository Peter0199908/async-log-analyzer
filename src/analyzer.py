import re
from datetime import datetime
from collections import defaultdict
from typing import Dict, List
from src.config import settings
from src.notifier import send_alert

LOG_PATTERN = re.compile(r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*(Failed password|HTTP 500)")

class LogAnalyzer:
    def __init__(self) -> None:
        self.failure_history: Dict[str, List[datetime]] = defaultdict(list)

    def process_line(self, log_line: str) -> str | None:
        match = LOG_PATTERN.search(log_line)
        return match.group("ip") if match else None

    async def check_alerts(self, ip: str) -> bool:
        current_time = datetime.now()
        self.failure_history[ip].append(current_time)
        self.failure_history[ip] = [t for t in self.failure_history[ip] if (current_time - t).total_seconds() <= settings.ALERT_TIME_WINDOW_SECONDS]

        if len(self.failure_history[ip]) >= settings.ALERT_THRESHOLD_COUNT:
            alert_msg = f"IP `{ip}` generated {len(self.failure_history[ip])} failures!"
            await send_alert(alert_msg)
            self.failure_history[ip].clear()
            return True
        return False