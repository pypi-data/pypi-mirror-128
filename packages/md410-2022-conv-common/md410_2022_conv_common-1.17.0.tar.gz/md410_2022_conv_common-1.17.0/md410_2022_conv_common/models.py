from datetime import datetime
from typing import Any, ClassVar, List, Optional

try:
    import constants
except ImportError:
    from . import constants

from pydantic import BaseModel


class AttendeeModel(BaseModel):
    first_names: str
    last_name: str
    name_badge: str
    cell: str
    email: str
    dietary: Optional[str]
    disability: Optional[str]
    first_mdc: bool
    mjf_lunch: bool
    lion: bool = None


class LionAttendeeModel(AttendeeModel):
    club: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.lion = True


class NonLionAttendeeModel(AttendeeModel):
    partner_program: bool

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.lion = False


class RegistrationItems(BaseModel):
    full: int = 0
    banquet: int = 0
    md_convention: int = 0
    theme: int = 0
    pins: int = 0


class Registration(BaseModel):
    reg_num: Optional[int]
    attendees: List[AttendeeModel]
    items: RegistrationItems
    timestamp: datetime
    cost: float = 0

    def __init__(self, **data: Any):
        super().__init__(**data)
        for field in ("full", "banquet", "md_convention", "theme", "pins"):
            self.cost += getattr(constants, f"COST_{field.upper()}", 0) * getattr(
                self.items, field, 0
            )
