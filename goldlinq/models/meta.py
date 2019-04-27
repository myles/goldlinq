from pathlib import Path
from typing import Union

from .microformats2 import HAdr, HCard, HEvent, HGeo


class ResultSet(list):
    """A list of items."""

    def __init__(self):
        super(ResultSet, self).__init__()

    @property
    def paths(self) -> list:
        """Returns a list of paths of the posts."""
        return [item.path for item in self if hasattr(item, "path")]

    @property
    def names(self) -> list:
        """Return a list of names of the posts."""
        return [item.name for item in self if hasattr(item, "name")]

    def order_by(
        self, field_name: str = "dt_taken", direction: str = "descending"
    ):
        """
        Order the results by a field.

        Parameters
        ----------

        field_name : str
            the field you want to order on

        direction : { 'descending', 'ascending' }
            what direction do you want to order by
        """
        reverse = False

        if direction.startswith("desc"):
            reverse = True

        if direction.startswith("asc"):
            reverse = False

        return self.sort(key=lambda x: getattr(x, field_name), reverse=reverse)


class Model:
    name = None
    h_type = None

    def __init__(self, path: Path):
        super(Model, self).__init__()

        self.path = Path(path)

    def __str__(self) -> str:
        if self.name:
            return self.name

    @property
    def url(self) -> str:
        raise NotImplementedError

    @classmethod
    def parse(cls, path: Path):
        raise NotImplementedError

    @classmethod
    def parse_directory(cls, path: Path):
        raise NotImplementedError

    @staticmethod
    def parse_location(data: dict) -> Union[HGeo, HAdr, HCard]:
        if not data.get("type"):
            raise ValueError

        if data.get("type") == "h-geo":
            return HGeo.parse(data)
        elif data.get("type") == "h-adr":
            return HAdr.parse(data)
        elif data.get("type") == "h-card":
            return HCard.parse(data)

    @staticmethod
    def parse_event(data: dict) -> HEvent:
        return HEvent.parse(data)

    def to_h_object(self) -> dict:
        h_object = {"type": self.h_type, "properties": {}}

        for key, value in self.__dict__.items():
            if key in ["path"]:
                continue

            if isinstance(value, (HAdr, HCard, HEvent, HGeo)):
                h_object["properties"][key] = [value.to_h_object()]
            else:
                h_object["properties"][key] = [value]

        return h_object
