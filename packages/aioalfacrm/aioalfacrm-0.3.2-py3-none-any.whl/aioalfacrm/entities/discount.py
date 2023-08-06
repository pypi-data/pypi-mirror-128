import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class Discount(AlfaEntity):
    branch_id: Optional[int] = fields.Integer()
    customer_id: Optional[int] = fields.Integer()
    discount_type: Optional[int] = fields.Integer()
    amount: Optional[int] = fields.Integer()
    note: Optional[str] = fields.String()
    subject_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    lesson_type_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    begin: Optional[datetime.date] = fields.DateField()
    end: Optional[datetime.date] = fields.DateField()

    def __init__(
            self,
            branch_id: Optional[int] = None,
            customer_id: Optional[int] = None,
            discount_type: Optional[int] = None,
            amount: Optional[int] = None,
            note: Optional[str] = None,
            subject_ids: Optional[List[int]] = None,
            lesson_type_ids: Optional[List[int]] = None,
            begin: Optional[datetime.date] = None,
            end: Optional[datetime.date] = None,
            **kwargs,
    ):
        super().__init__(
            branch_id=branch_id,
            customer_id=customer_id,
            discount_type=discount_type,
            amount=amount,
            note=note,
            subject_ids=subject_ids,
            lesson_type_ids=lesson_type_ids,
            begin=begin,
            end=end,
            **kwargs,
        )
