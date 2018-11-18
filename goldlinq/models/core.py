"""Content type models."""
import datetime
import re
from pathlib import Path

import toml

from flask import url_for

from .meta import Model, ResultSet

GALLERY_FOLDER_REGEX = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>[\w-]+)$"
)


class Photo(Model):
    """
    An individual photo object.

    Arguments
    ---------

    path : Path
        full path to the photo's TOML file.
    """

    @property
    def gallery(self):
        return Gallery.parse(self.path.parents[1])

    @classmethod
    def parse(cls, path):
        path = Path(path)
        photo = cls(path)

        if not (path.is_file() or path.suffix == ".toml"):
            raise ValueError

        with path.open() as file_obj:
            meta = toml.loads(file_obj.read())

        for key, value in meta.items():
            if key == "location":
                setattr(photo, key, photo.parse_location(value))
            elif key == "event":
                setattr(photo, key, photo.parse_event(value))
            else:
                setattr(photo, key, value)

        setattr(photo, "slug", path.name.replace(path.suffix, ""))

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

    @property
    def url(self):
        return url_for("views.gallery_detail", gallery_slug=self.slug)

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

        for key, value in meta.items():
            if key == "location":
                setattr(gallery, key, gallery.parse_location(value))
            elif key == "event":
                setattr(gallery, key, gallery.parse_event(value))
            else:
                setattr(gallery, key, value)

        if content_file_path.is_file():
            with content_file_path.open() as content_file_obj:
                setattr(gallery, "content", content_file_obj.read())

        slug = gallery_folder_regex.group("slug")
        setattr(gallery, "slug", slug)

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
