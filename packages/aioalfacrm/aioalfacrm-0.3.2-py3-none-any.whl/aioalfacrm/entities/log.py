import datetime
from typing import Dict, Any

from .. import fields
from ..core import AlfaEntity


class Log(AlfaEntity):
    entity: str = fields.String()
    entity_id: int = fields.Integer()
    user_id: int = fields.Integer()
    event: int = fields.Integer()
    fields_old: Dict[str, Any] = fields.DictField()
    fields_new: Dict[str, Any] = fields.DictField()
    fields_rel: Dict[str, Any] = fields.DictField()
    date_time: datetime.datetime = fields.DateTimeField()

    def __init__(
            self,
            entity: str = None,
            entity_id: int = None,
            user_id: int = None,
            event: int = None,
            fields_old: Dict[str, Any] = None,
            fields_new: Dict[str, Any] = None,
            fields_rel: Dict[str, Any] = None,
            date_time: datetime.datetime = None,
            **kwargs,
    ):
        super().__init__(
            entity=entity,
            entity_id=entity_id,
            user_id=user_id,
            event=event,
            fields_old=fields_old,
            fields_new=fields_new,
            fields_rel=fields_rel,
            date_time=date_time,
            **kwargs
        )
