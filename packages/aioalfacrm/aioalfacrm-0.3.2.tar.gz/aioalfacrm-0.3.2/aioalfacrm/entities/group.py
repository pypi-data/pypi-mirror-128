import datetime
from typing import Optional, List

from .. import fields
from ..core.entity import AlfaEntity


class Group(AlfaEntity):
    branch_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    teacher_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    name: Optional[str] = fields.String()
    level_id: Optional[int] = fields.Integer()
    status_id: Optional[int] = fields.Integer()
    company_id: Optional[int] = fields.Integer()
    streaming_id: Optional[int] = fields.Integer()
    limit: Optional[int] = fields.Integer()
    note: Optional[str] = fields.String()
    b_date: Optional[datetime.date] = fields.DateField()
    e_date: Optional[datetime.date] = fields.DateField()

    def __init__(self,
                 branch_ids: Optional[List[int]] = None,
                 teacher_ids: Optional[List[int]] = None,
                 name: Optional[str] = None,
                 level_id: Optional[int] = None,
                 status_id: Optional[int] = None,
                 company_id: Optional[int] = None,
                 streaming_id: Optional[int] = None,
                 limit: Optional[int] = None,
                 note: Optional[str] = None,
                 b_date: Optional[datetime.date] = None,
                 e_date: Optional[datetime.date] = None,
                 **kwargs,
                 ):
        print(locals())
        super().__init__(
            branch_ids=branch_ids,
            teacher_ids=teacher_ids,
            name=name,
            level_id=level_id,
            status_id=status_id,
            company_id=company_id,
            streaming_id=streaming_id,
            limit=limit,
            note=note,
            b_date=b_date,
            e_date=e_date,
            **kwargs
        )
