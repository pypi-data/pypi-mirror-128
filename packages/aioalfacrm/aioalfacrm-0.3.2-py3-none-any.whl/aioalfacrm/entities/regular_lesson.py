import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class RegularLesson(AlfaEntity):
    branch_id: Optional[int] = fields.Integer()
    lesson_type_id: Optional[int] = fields.Integer()
    related_class: Optional[str] = fields.String()
    related_id: Optional[int] = fields.Integer()
    subject_id: Optional[int] = fields.Integer()
    streaming: Optional[bool] = fields.Bool()
    teacher_ids: Optional[list] = fields.ListField(fields.Integer())
    room_id: Optional[int] = fields.Integer()
    day: Optional[int] = fields.Integer()
    days: Optional[List[int]] = fields.ListField(fields.Integer())
    time_from_v: Optional[datetime.time] = fields.TimeField()
    time_to_v: Optional[datetime.time] = fields.TimeField()
    e_date_v: Optional[datetime.date] = fields.DateField()
    b_date_v: Optional[datetime.date] = fields.DateField()
    b_date: Optional[datetime.date] = fields.DateField()
    e_date: Optional[datetime.date] = fields.DateField()
    is_public: Optional[bool] = fields.Bool()

    def __init__(
            self,
            branch_id: Optional[int] = None,
            lesson_type_id: Optional[int] = None,
            related_class: Optional[str] = None,
            related_id: Optional[int] = None,
            subject_id: Optional[int] = None,
            streaming: Optional[bool] = None,
            teacher_ids: Optional[List[int]] = None,
            room_id: Optional[int] = None,
            day: Optional[int] = None,
            days: Optional[List[int]] = None,
            time_from_v: Optional[datetime.time] = None,
            time_to_v: Optional[datetime.time] = None,
            e_date_v: Optional[datetime.date] = None,
            b_date_v: Optional[datetime.date] = None,
            b_date: Optional[datetime.date] = None,
            e_date: Optional[datetime.date] = None,
            is_public: Optional[bool] = None,
            **kwargs
    ):
        super().__init__(
            branch_id=branch_id,
            lesson_type_id=lesson_type_id,
            related_class=related_class,
            related_id=related_id,
            subject_id=subject_id,
            streaming=streaming,
            teacher_ids=teacher_ids,
            room_id=room_id,
            day=day,
            days=days,
            time_from_v=time_from_v,
            time_to_v=time_to_v,
            e_date_v=e_date_v,
            b_date_v=b_date_v,
            b_date=b_date,
            e_date=e_date,
            is_public=is_public,
            **kwargs
        )
