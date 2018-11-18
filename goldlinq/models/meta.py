from pathlib import Path

from .microformats2 import HAdr, HCard, HEvent, HGeo


class ResultSet(list):
    """A list of items."""

    def __init__(self):
        super(ResultSet, self).__init__()

    @property
    def paths(self):
        """Returns a list of paths of the posts."""
        return [item.path for item in self if hasattr(item, "path")]

    @property
    def names(self):
        """Return a list of names of the posts."""
        return [item.name for item in self if hasattr(item, "name")]

    def order_by(self, field_name="dt_taken", direction="descending"):
        """
        Order the results by a field.

        Parameters
        ----------

        field_name : str
            the field you want to order on

        direction : { 'descending', 'ascending' }
            what direction do you want to order by
        """
        if direction.startswith("desc"):
            reverse = True
        elif direction.startswith("asc"):
            reverse = False
        else:
            reverse = False

        return self.sort(key=lambda x: getattr(x, field_name), reverse=reverse)


class Model:
    def __init__(self, path):
        super(Model, self).__init__()

        self.path = Path(path)

    def __str__(self):
        if self.name:
            return self.name

    @property
    def url(self):
        raise NotImplementedError

    @classmethod
    def parse(cls, path):
        raise NotImplementedError

    @classmethod
    def parse_directory(cls, path):
        raise NotImplementedError

    @staticmethod
    def parse_location(data):
        if not data.get("type"):
            raise ValueError

        if data.get("type") == "h-geo":
            return HGeo.parse(data)
        elif data.get("type") == "h-adr":
            return HAdr.parse(data)
        elif data.get("type") == "h-card":
            return HCard.parse(data)

    @staticmethod
    def parse_event(data):
        return HEvent.parse(data)
