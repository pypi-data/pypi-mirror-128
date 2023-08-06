from typing import Optional

from .. import fields
from ..core import AlfaEntity


class LeadSource(AlfaEntity):
    code: Optional[str] = fields.String()
    name: Optional[str] = fields.String()
    is_enabled: Optional[bool] = fields.Bool()
    weight: Optional[int] = fields.Integer()

    def __init__(
            self,
            code: Optional[str] = None,
            name: Optional[str] = None,
            is_enabled: Optional[bool] = None,
            weight: Optional[int] = None,
            **kwargs,
    ):
        super(LeadSource, self).__init__(
            code=code,
            name=name,
            is_enabled=is_enabled,
            weight=weight,
            **kwargs,
        )
