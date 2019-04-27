from flask import Blueprint, render_template, current_app, jsonify

from .pagination import Paginator
from .models import Gallery

BLUEPRINT = Blueprint(
    "views",
    __name__,
)


@BLUEPRINT.route("/")
@BLUEPRINT.route("/<int:page>/")
def gallery_list(page=1):
    gallery_list = Gallery.parse_directory(current_app.config["GALLERIES_PATH"])
    gallery_list.order_by("dt_published")

    paginator = Paginator(gallery_list, current_app.config["PER_PAGE"])
    page = paginator.get_page(page)

    return render_template("gallery/list.html", gallery_list=page)


@BLUEPRINT.route("/<path:gallery_slug>/")
def gallery_detail(gallery_slug):
    gallery_obj = Gallery.parse(
        current_app.config["GALLERIES_PATH"].joinpath(gallery_slug)
    )

    return render_template("gallery/detail.html", gallery=gallery_obj)


@BLUEPRINT.route("/<path:gallery_slug>/json/")
def gallery_detail_json(gallery_slug):
    gallery_obj = Gallery.parse(
        current_app.config["GALLERIES_PATH"].joinpath(gallery_slug)
    )

    return jsonify(gallery_obj.to_h_object())


@BLUEPRINT.route("/<path:gallery_slug>/<path:photo_slug>/")
def photo_detail(gallery_slug, photo_slug):
    gallery_obj = Gallery.parse(
        current_app.config["GALLERIES_PATH"].joinpath(gallery_slug)
    )

    photo_obj = gallery_obj.get_photo(photo_slug)

    return render_template(
        "gallery/photos/detail.html", gallery=gallery_obj, photo=photo_obj
    )


@BLUEPRINT.route("/<path:gallery_slug>/<path:photo_slug>/json/")
def photo_detail_json(gallery_slug, photo_slug):
    gallery_obj = Gallery.parse(
        current_app.config.GALLERIES_PATH.joinpath(gallery_slug)
    )

    photo_obj = gallery_obj.get_photo(photo_slug)

    return jsonify(photo_obj.to_h_object())
