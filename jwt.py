''' Class to hold information about heartbeat '''
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Heartbeat:
    identifier: int
    created_at: datetime
    created_by: str
    creator_ip: str
    creator_ver: str
