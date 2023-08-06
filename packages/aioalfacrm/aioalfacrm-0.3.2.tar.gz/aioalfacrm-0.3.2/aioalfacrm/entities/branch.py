from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class Branch(AlfaEntity):
    name: Optional[str] = fields.String()
    is_active: Optional[bool] = fields.Bool()
    subject_ids: Optional[List[int]] = fields.ListField(base=fields.Integer())
    weight: Optional[int] = fields.Integer()

    def __init__(
            self,
            name: Optional[str] = '',
            is_active: Optional[bool] = True,
            subject_ids: Optional[List[int]] = None,
            weight: Optional[int] = None,
            **kwargs,
    ):
        super(Branch, self).__init__(
            name=name,
            is_active=is_active,
            subject_ids=subject_ids,
            weight=weight,
            **kwargs
        )
