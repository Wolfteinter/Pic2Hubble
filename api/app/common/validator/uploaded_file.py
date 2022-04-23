from http import HTTPStatus

from flask import request

from api.app.common.constants import ALLOWED_IMAGE_EXTENSIONS


def is_valid_image(filename: str):

    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def validate_input_image(funct):

    def validator(*args, **kwargs):
        if "image" not in request.files or not request.files["image"]:
            return {"message": "image is required"}, HTTPStatus.BAD_REQUEST

        if not is_valid_image(request.files["image"].filename):
            return (
                {"message": "image format not supported, try jpg, jpeg or png"}, 
                HTTPStatus.BAD_REQUEST
            )

        return funct(*args, **kwargs)

    return validator