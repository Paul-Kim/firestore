from firestore.errors import ValidationError
from firestore.datatypes.base import Base


class String(Base):

    __slots__ = (
        "minimum",
        "maximum",
        "coerce",
        "_name",
        "value"
    )

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get("minimum")
        self.maximum = kwargs.get("maximum")
        self.coerce = kwargs.get("coerce", True)
        super(String, self).__init__(*args, **kwargs)

    def validate(self, value):
        max_msg = f"{self._name} must have a maximum len of {self.maximum}, found {len(value)}"
        min_msg = (
            f"{self._name} must have minimum len of {self.minimum}, found {len(value)}"
        )

        if self.minimum and self.minimum > len(value):
            raise ValidationError(min_msg)
        if self.maximum and self.maximum < len(value):
            raise ValidationError(max_msg)
        if self.required and not value:
            raise ValidationError(f"{self._name} is a required field")
        if isinstance(value, str):
            return value
        if not isinstance(value, str) and self.coerce:
            if isinstance(value, int) or isinstance(value, float):
                return str(value)
            raise ValueError(f"Can not coerce {type(value)} to str")
        raise ValueError(f"{value} is not of type str and coerce is {self.coerce}")
