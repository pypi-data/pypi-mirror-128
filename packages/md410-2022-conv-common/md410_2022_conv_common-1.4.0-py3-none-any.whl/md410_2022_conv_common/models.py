from pydantic import BaseModel
from typing import Optional, List


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


class LionAttendeeModel(AttendeeModel):
    club: str


class NonLionAttendeeModel(AttendeeModel):
    partner_program: bool


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
