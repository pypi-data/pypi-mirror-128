import datetime
from typing import Optional

from .. import fields
from ..core import AlfaEntity


class Communication(AlfaEntity):
    type_id: Optional[int] = fields.Integer()
    related_class: Optional[str] = fields.String(alias='class')
    related_id: Optional[int] = fields.Integer()
    user_id: Optional[int] = fields.Integer()
    added: Optional[datetime.datetime] = fields.DateTimeField()
    comment: Optional[str] = fields.String()

    def __init__(
            self,
            type_id: Optional[int] = None,
            related_class: Optional[str] = None,
            related_id: Optional[int] = None,
            user_id: Optional[int] = None,
            added: Optional[datetime.datetime] = None,
            comment: Optional[str] = None,
            **kwargs,
    ):
        super().__init__(
            type_id=type_id,
            related_class=related_class,
            related_id=related_id,
            user_id=user_id,
            added=added,
            comment=comment,
            **kwargs,
        )
