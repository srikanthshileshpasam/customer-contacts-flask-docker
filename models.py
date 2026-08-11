from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Contact:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    company: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def validate(self) -> list[str]:
        errors = []
        if not self.name.strip():
            errors.append("Name is required")
        if not self.email.strip() or "@" not in self.email:
            errors.append("A valid email is required")
        return errors