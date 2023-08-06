from typing import Optional

from .. import fields
from ..core import AlfaEntity


class LeadStatus(AlfaEntity):
    name: Optional[str] = fields.String()
    is_enabled: Optional[bool] = fields.Bool()
    weight: Optional[int] = fields.Integer()

    def __init__(
            self,
            name: Optional[str] = None,
            is_enabled: Optional[bool] = None,
            weight: Optional[int] = None,
            **kwargs,
    ):
        super(LeadStatus, self).__init__(
            name=name,
            is_enabled=is_enabled,
            weight=weight,
            **kwargs,
        )
