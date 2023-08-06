from typing import Optional

from .. import fields
from ..core import AlfaEntity


class Location(AlfaEntity):
    branch_id: Optional[int] = fields.Integer()
    is_active: Optional[bool] = fields.Bool()
    name: Optional[str] = fields.String()
    weight: Optional[int] = fields.Integer()

    def __init__(
            self,
            branch_id: Optional[int] = None,
            is_active: Optional[bool] = None,
            name: Optional[str] = None,
            **kwargs,
    ):
        super(Location, self).__init__(
            branch_id=branch_id,
            is_active=is_active,
            name=name,
            **kwargs,
        )
