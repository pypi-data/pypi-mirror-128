from typing import Optional, List

from .. import fields
from ..core import AlfaEntity


class PayAccount(AlfaEntity):
    branch_id: Optional[int] = fields.Integer()
    name: Optional[str] = fields.String()
    user_ids: Optional[List[int]] = fields.ListField(fields.Integer())
    is_enabled: Optional[bool] = fields.Bool()
    weight: Optional[int] = fields.Integer()

    def __init__(
            self,
            branch_id: Optional[int] = None,
            name: Optional[str] = None,
            user_ids: Optional[List[int]] = None,
            is_enabled: Optional[bool] = None,
            weight: Optional[int] = None,
            **kwargs
    ):
        super().__init__(
            branch_id=branch_id,
            name=name,
            user_ids=user_ids,
            is_enabled=is_enabled,
            weight=weight,
            **kwargs
        )
