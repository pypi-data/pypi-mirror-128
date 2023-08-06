import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class CustomerTariff(AlfaEntity):
    customer_id: Optional[int] = fields.Integer()
    tariff_id: Optional[int] = fields.Integer()
    subject_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    lesson_type_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    is_separate_balance: Optional[bool] = fields.Bool()
    balance: Optional[float] = fields.Float()
    paid_count: Optional[int] = fields.Integer()
    paid_till: Optional[datetime.datetime] = fields.DateTimeField()
    note: Optional[str] = fields.String()
    b_date: Optional[datetime.date] = fields.DateField()
    e_date: Optional[datetime.date] = fields.DateField()
    paid_lesson_count: Optional[int] = fields.Integer()

    def __init__(
            self,
            customer_id: Optional[int] = None,
            tariff_id: Optional[int] = None,
            subject_ids: Optional[List[int]] = None,
            lesson_type_ids: Optional[List[int]] = None,
            is_separeated_balance: Optional[bool] = None,
            balance: Optional[float] = None,
            paid_count: Optional[int] = None,
            paid_till: Optional[datetime.datetime] = None,
            note: Optional[str] = None,
            b_date: Optional[datetime.date] = None,
            e_date: Optional[datetime.date] = None,
            paid_lesson_count: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(
            customer_id=customer_id,
            tariff_id=tariff_id,
            subject_ids=subject_ids,
            lesson_type_ids=lesson_type_ids,
            is_separeated_balance=is_separeated_balance,
            balance=balance,
            paid_count=paid_count,
            paid_till=paid_till,
            note=note,
            b_date=b_date,
            e_date=e_date,
            paid_lesson_count=paid_lesson_count,
            **kwargs,
        )
