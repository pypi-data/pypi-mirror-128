from typing import Optional

from .. import fields
from ..core import AlfaEntity


class Subject(AlfaEntity):
    name: Optional[str] = fields.String()
    weight: Optional[int] = fields.Integer()

    def __init__(
            self,
            name: Optional[str] = None,
            weight: Optional[int] = None,
            **kwargs,
    ):
        super(Subject, self).__init__(
            name=name,
            weight=weight,
            **kwargs,
        )
