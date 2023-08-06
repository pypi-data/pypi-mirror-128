import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class Lesson(AlfaEntity):
    branch_id: Optional[int] = fields.Integer()
    date: Optional[datetime.date] = fields.DateField()
    time_from: Optional[datetime.datetime] = fields.DateTimeField()
    time_to: Optional[datetime.datetime] = fields.DateTimeField()
    lesson_type_id: Optional[int] = fields.Integer()
    status: Optional[int] = fields.Integer()
    subject_id: Optional[int] = fields.Integer()
    room_id: Optional[int] = fields.Integer()
    teacher_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    customer_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    group_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    streaming: Optional[bool] = fields.Bool()
    note: Optional[str] = fields.String()

    def __init__(
            self,
            branch_id: Optional[int] = None,
            date: Optional[datetime.date] = None,
            time_from: Optional[datetime.datetime] = None,
            time_to: Optional[datetime.datetime] = None,
            lesson_type_id: Optional[int] = None,
            status: Optional[int] = None,
            subject_id: Optional[int] = None,
            room_id: Optional[int] = None,
            teacher_ids: Optional[List[int]] = None,
            customer_ids: Optional[List[int]] = None,
            group_ids: Optional[List[int]] = None,
            streaming: Optional[bool] = None,
            note: Optional[str] = None,
            **kwargs,
    ):
        super().__init__(
            branch_id=branch_id,
            date=date,
            time_from=time_from,
            time_to=time_to,
            lesson_type_id=lesson_type_id,
            status=status,
            subject_id=subject_id,
            room_id=room_id,
            teacher_ids=teacher_ids,
            customer_ids=customer_ids,
            group_ids=group_ids,
            streaming=streaming,
            note=note,
            **kwargs
        )
