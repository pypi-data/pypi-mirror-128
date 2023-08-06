import datetime
from typing import Optional

from .. import fields
from ..core import AlfaEntity


class Pay(AlfaEntity):
    branch_id: Optional[int] = fields.Integer()
    location_id: Optional[int] = fields.Integer()
    customer_id: Optional[int] = fields.Integer()
    pay_type_id: Optional[int] = fields.Integer()
    pay_account_id: Optional[int] = fields.Integer()
    pay_item_id: Optional[int] = fields.Integer()
    teacher_id: Optional[int] = fields.Integer()
    commodity_id: Optional[int] = fields.Integer()
    ctt_id: Optional[int] = fields.Integer()
    document_date: Optional[datetime.date] = fields.DateField()
    income: Optional[float] = fields.Float()
    payer_name: Optional[str] = fields.String()
    note: Optional[str] = fields.String()
    is_confirmed: Optional[bool] = fields.Bool()
    custom_md_order: Optional[str] = fields.String()
    custom_order_description: Optional[str] = fields.String()

    def __init__(
            self,
            branch_id: Optional[int] = None,
            location_id: Optional[int] = None,
            customer_id: Optional[int] = None,
            pay_type_id: Optional[int] = None,
            pay_account_id: Optional[int] = None,
            pay_item_id: Optional[int] = None,
            teacher_id: Optional[int] = None,
            commodity_id: Optional[int] = None,
            ctt_id: Optional[int] = None,
            document_date: Optional[datetime.date] = None,
            income: Optional[float] = None,
            payer_name: Optional[str] = None,
            note: Optional[str] = None,
            is_confirmed: Optional[bool] = None,
            custom_md_order: Optional[str] = None,
            custom_order_description: Optional[str] = None,
            **kwargs
    ):
        super().__init__(
            branch_id=branch_id,
            location_id=location_id,
            customer_id=customer_id,
            pay_type_id=pay_type_id,
            pay_account_id=pay_account_id,
            pay_item_id=pay_item_id,
            teacher_id=teacher_id,
            commodity_id=commodity_id,
            ctt_id=ctt_id,
            document_date=document_date,
            income=income,
            payer_name=payer_name,
            note=note,
            is_confirmed=is_confirmed,
            custom_md_order=custom_md_order,
            custom_order_description=custom_order_description,
            **kwargs
        )
