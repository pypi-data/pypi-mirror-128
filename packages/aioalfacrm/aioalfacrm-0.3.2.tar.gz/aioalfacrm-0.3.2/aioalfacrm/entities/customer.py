import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class Customer(AlfaEntity):
    name: Optional[str] = fields.String()
    branch_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    teacher_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    is_study: Optional[bool] = fields.Bool()
    study_status_id: Optional[int] = fields.Integer()
    lead_status_id: Optional[int] = fields.Integer()
    lead_reject_id: Optional[int] = fields.Integer()
    lead_source_id: Optional[int] = fields.Integer()
    assigned_id: Optional[int] = fields.Integer()
    legal_type: Optional[int] = fields.Integer()
    legal_name: Optional[str] = fields.String()
    company_id: Optional[int] = fields.Integer()
    dob: Optional[datetime.date] = fields.DateField()
    balance: Optional[float] = fields.Float()
    balance_base: Optional[float] = fields.Float()
    balance_bonus: Optional[float] = fields.Float()
    last_attend_date: Optional[datetime.date] = fields.DateField()
    b_date: Optional[datetime.datetime] = fields.DateTimeField()
    e_date: Optional[datetime.datetime] = fields.DateField()
    paid_count: Optional[int] = fields.Integer()
    paid_lesson_count: Optional[int] = fields.Integer()
    paid_lesson_date: Optional[datetime.datetime] = fields.DateTimeField()
    next_lesson_date: Optional[datetime.datetime] = fields.DateTimeField()
    paid_till: Optional[datetime.datetime] = fields.DateTimeField()
    phone: Optional[List[str]] = fields.ListField(fields.String())
    email: Optional[List[str]] = fields.ListField(fields.String())
    web: Optional[List[str]] = fields.ListField(fields.String())
    addr: Optional[List[str]] = fields.ListField(fields.String())
    note: Optional[List[str]] = fields.String()
    color: Optional[str] = fields.String()

    def __init__(
            self,
            name: Optional[str] = None,
            branch_ids: Optional[List[int]] = None,
            teacher_ids: Optional[List[int]] = None,
            is_study: Optional[bool] = None,
            study_status_id: Optional[int] = None,
            lead_reject_id: Optional[int] = None,
            lead_status_id: Optional[int] = None,
            assigned_id: Optional[int] = None,
            legal_type: Optional[int] = None,
            legal_name: Optional[str] = None,
            company_id: Optional[int] = None,
            dob: Optional[datetime.date] = None,
            balance: Optional[float] = None,
            balance_base: Optional[float] = None,
            balance_bonus: Optional[float] = None,
            last_attend_date: Optional[datetime.date] = None,
            b_date: Optional[datetime.datetime] = None,
            e_date: Optional[datetime.date] = None,
            paid_count: Optional[int] = None,
            paid_lesson_count: Optional[int] = None,
            paid_lesson_date: Optional[datetime.datetime] = None,
            next_lesson_date: Optional[datetime.datetime] = None,
            paid_till: Optional[datetime.datetime] = None,
            phone: Optional[List[str]] = None,
            email: Optional[List[str]] = None,
            web: Optional[List[str]] = None,
            addr: Optional[List[str]] = None,
            note: Optional[str] = None,
            color: Optional[str] = None,
            **kwargs,
    ):
        super(Customer, self).__init__(
            name=name,
            branch_ids=branch_ids,
            teacher_ids=teacher_ids,
            is_study=is_study,
            study_status_id=study_status_id,
            lead_status_id=lead_status_id,
            lead_reject_id=lead_reject_id,
            assigned_id=assigned_id,
            legal_type=legal_type,
            legal_name=legal_name,
            company_id=company_id,
            dob=dob,
            balance=balance,
            balance_base=balance_base,
            balance_bonus=balance_bonus,
            last_attend_date=last_attend_date,
            b_date=b_date,
            e_date=e_date,
            paid_count=paid_count,
            paid_lesson_count=paid_lesson_count,
            paid_lesson_date=paid_lesson_date,
            next_lesson_date=next_lesson_date,
            paid_till=paid_till,
            phone=phone,
            email=email,
            web=web,
            addr=addr,
            note=note,
            color=color,
            **kwargs,
        )
