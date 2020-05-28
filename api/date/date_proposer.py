from datetime import datetime
from typing import List

from api.date.proposer import Proposer
from api.date.window import Window
from api.libs.db.store import Store


class DateProposer(Proposer):
    def __init__(self, store: Store):
        self.store = store
    
    def propose(self, date: datetime, participants: List[str]) -> List[Window]:
        return [Window(start=datetime.now(), end=datetime.now())]
