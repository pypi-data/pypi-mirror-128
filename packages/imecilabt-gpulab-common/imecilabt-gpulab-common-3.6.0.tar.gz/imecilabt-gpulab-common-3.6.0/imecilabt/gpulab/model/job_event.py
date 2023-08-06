import datetime
import logging

import dateutil.parser
from enum import Enum
from typing import Optional, Union

from imecilabt.gpulab.model.job import JobState as Job1State
from imecilabt.gpulab.model.job2 import JobStatus as Job2Status


class JobEventType(Enum):
    STATUS_CHANGE = 'Status Change'
    DEBUG = 'Debug'
    INFO = 'Info'
    WARN = 'Warning'
    ERROR = 'Error'

_levelToJobEventType = {
    logging.CRITICAL: JobEventType.ERROR,
    logging.ERROR: JobEventType.ERROR,
    logging.WARNING: JobEventType.WARN,
    logging.INFO: JobEventType.INFO,
    logging.DEBUG: JobEventType.DEBUG
}
def logginglevel_to_jobeventype(level: int) -> JobEventType:
    if level in _levelToJobEventType:
        return _levelToJobEventType[level]
    else:
        return JobEventType.DEBUG

class JobEvent:
    def __init__(self,
                 job_id: str,
                 type: JobEventType,
                 time: datetime.datetime = None,
                 new_state1_or_status2: Union[Job1State, Job2Status, None] = None,
                 msg: Optional[str] = None,
                 ):
        assert isinstance(job_id, str)
        self.job_id = job_id
        self.type = type
        self.time = time if time is not None else datetime.datetime.now(datetime.timezone.utc)
        assert new_state1_or_status2 is None or \
               isinstance(new_state1_or_status2, Job1State) or \
               isinstance(new_state1_or_status2, Job2Status)
        self.new_state1_or_status2 = new_state1_or_status2
        self.msg = msg

    def to_dict(self) -> dict:
        res = dict()
        res['job_id'] = self.job_id
        res['type'] = self.type.name if self.type else None
        res['time'] = self.time.isoformat() if self.time else None
        res['new_state'] = self.new_status.name if self.new_status else None
        res['msg'] = self.msg
        return res

    @property
    def new_status(self):
        return Job2Status[self.new_state1_or_status2.name] if self.new_state1_or_status2 else None

    # @property
    # def new_state(self):
    #     return Job1State[self.new_state1_or_status2.name] if self.new_state1_or_status2 else None

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            d['job_id'],
            JobEventType[d['type']] if 'type' in d else None,
            dateutil.parser.parse(d['time']) if 'time'in d and d['time'] else None,
            Job1State[d['new_status']] if 'new_status' in d and d['new_status'] else None,
            d['msg']
        )
