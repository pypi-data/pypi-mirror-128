from typing import Any, Dict

from ..core import AlfaEntity
from .. import fields
import datetime as dt


class Webhook(AlfaEntity):
    branch_id: int = fields.Integer(editable=False)
    event: str = fields.String(editable=False)
    entity: str = fields.String(editable=False)
    entity_id: int = fields.Integer(editable=False)
    fields_old: Dict[str, Any] = fields.DictField(editable=False)
    fields_new: Dict[str, Any] = fields.DictField(editable=False)
    fields_rel: Dict[str, Any] = fields.DictField(editable=False)
    user_id: int = fields.Integer(editable=False)
    datetime: dt.datetime = fields.DateTimeField(editable=False)

    def __init__(self,
                 branch_id: int,
                 event: str,
                 entity: str,
                 entity_id: int,
                 fields_old: Dict[str, Any],
                 fields_new: Dict[str, Any],
                 fields_rel: Dict[str, Any],
                 user_id: int,
                 datetime: dt.datetime,
                 **kwargs):
        super().__init__(
            branch_id=branch_id,
            event=event,
            entity=entity,
            entity_id=entity_id,
            fields_old=fields_old,
            fields_new=fields_new,
            fields_rel=fields_rel,
            user_id=user_id,
            datetime=datetime,
            **kwargs
        )
