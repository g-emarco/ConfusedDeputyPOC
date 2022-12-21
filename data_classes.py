from dataclasses import dataclass
from uuid import UUID


@dataclass
class Organization:
    name: str
    id: UUID
    target_service_account_email: str
    deputy_service_account_email: str = ""

    def __str__(self):
        return self.name
