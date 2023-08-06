import datetime
from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class Task(AlfaEntity):
    company_id: Optional[int] = fields.Integer()
    branch_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    user_id: Optional[int] = fields.Integer()
    assigned_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    group_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    customer_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    title: Optional[str] = fields.String()
    text: Optional[str] = fields.String()
    is_archive: Optional[bool] = fields.Bool()
    created_at: Optional[datetime.datetime] = fields.DateTimeField()
    is_done: Optional[bool] = fields.Bool()
    is_private: Optional[bool] = fields.Bool()
    due_date: Optional[datetime.date] = fields.DateField()
    done_date: Optional[datetime.datetime] = fields.DateTimeField()
    is_public_entry: Optional[bool] = fields.Bool()
    is_notify: Optional[bool] = fields.Bool()
    priority: Optional[int] = fields.Integer()

    def __init__(
            self,
            company_id: Optional[int] = None,
            branch_ids: Optional[List[int]] = None,
            user_id: Optional[int] = None,
            assigned_ids: Optional[List[int]] = None,
            group_ids: Optional[List[int]] = None,
            customer_ids: Optional[List[int]] = None,
            title: Optional[str] = None,
            text: Optional[str] = None,
            is_archive: Optional[bool] = None,
            created_at: Optional[datetime.datetime] = None,
            is_done: Optional[bool] = None,
            is_private: Optional[bool] = None,
            due_date: Optional[datetime.date] = None,
            done_date: Optional[datetime.datetime] = None,
            is_public_entry: Optional[bool] = None,
            is_notify: Optional[bool] = None,
            priority: Optional[int] = None,
            **kwargs
    ):
        super().__init__(
            company_id=company_id,
            branch_ids=branch_ids,
            user_id=user_id,
            assigned_ids=assigned_ids,
            group_ids=group_ids,
            customer_ids=customer_ids,
            title=title,
            text=text,
            is_archive=is_archive,
            created_at=created_at,
            is_done=is_done,
            is_private=is_private,
            due_date=due_date,
            done_date=done_date,
            is_public_entry=is_public_entry,
            is_notify=is_notify,
            priority=priority,
            **kwargs
        )
