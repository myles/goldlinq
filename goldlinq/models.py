"""Content type models."""
import datetime
import re
from pathlib import Path

import toml

GALLERY_FOLDER_REGEX = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>[\w-]+)$"
)


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

    @classmethod
    def parse(cls, path):
        raise NotImplementedError

    @classmethod
    def parse_directory(cls, path):
        raise NotImplementedError


class Photo(Model):
    """
    An individual photo object.

    Arguments
    ---------

    path : Path
        full path to the photo's TOML file.
    """

    @classmethod
    def parse(cls, path):
        path = Path(path)
        photo = cls(path)

        if not (path.is_file() or path.suffix == ".toml"):
            raise ValueError

        with path.open() as file_obj:
            meta = toml.loads(file_obj.read())

        for key, value in meta.items():
            setattr(photo, key, value)

        return photo

    @classmethod
    def parse_directory(cls, path):
        results = ResultSet()
        path = Path(path)

        for toml_file_path in path.glob("*.toml"):
            results.append(cls.parse(toml_file_path))

        return results


class Gallery(Model):
    """
    An individual gallery object.

    Arguments
    ---------

    path : Path
        full path to the gallery's directory.
    """

    @classmethod
    def parse(cls, path):
        gallery_path = Path(path)
        meta_file_path = Path(path).joinpath("meta.toml")
        content_file_path = Path(path).joinpath("content.md")

        gallery = cls(gallery_path)

        if not meta_file_path.is_file():
            raise ValueError

        with meta_file_path.open() as meta_file_obj:
            meta = toml.loads(meta_file_obj.read())

        gallery_folder_regex = GALLERY_FOLDER_REGEX.match(gallery_path.name)

        if not meta.get("dt_published"):
            dt_published = datetime.datetime.fromisoformat(
                "{year}-{month}-{day}".format(
                    **gallery_folder_regex.groupdict()
                )
            )

            setattr(gallery, "dt_published", dt_published)

        if not meta.get("slug"):
            slug = gallery_folder_regex.group("slug")
            setattr(gallery, "slug", slug)

        for key, value in meta.items():
            setattr(gallery, key, value)

        if content_file_path.is_file():
            with content_file_path.open() as content_file_obj:
                setattr(gallery, "content", content_file_obj.read())

        return gallery

    @classmethod
    def parse_directory(cls, path):
        results = ResultSet()
        path = Path(path)

        for directory in path.glob("**/meta.toml"):
            results.append(cls.parse(directory.parent))

        return results

    def list_photo(self):
        return Photo.parse_directory(self.path.joinpath("photos"))

    def get_photo(self, photo):
        return Photo.parse(self.path.joinpath("photos/", photo))
