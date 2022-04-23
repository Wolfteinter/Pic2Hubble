from http import HTTPStatus

from flask import current_app, request
from flask_restful import Resource
from PIL import Image

from api.app.common.algos.pict_to_x import AlgoPict2X
from api.app.common.utils import image_to_base64
from api.app.common.validator.uploaded_file import validate_input_image
from api.app.ext import dataset_hubble_v1_0, metadata_hubble_v1_0 


algo = AlgoPict2X(dataset_hubble_v1_0, metadata_hubble_v1_0)


class Generator(Resource):

    @validate_input_image
    def post(self):
        file = request.files["image"]
        img = Image.open(file.stream)

        if img.mode != "RGB":
            return (
                {"message": "Space color not supported, try only RGB"},
                HTTPStatus.BAD_REQUEST
            )

        current_app.logger.info(
            f"New image {img.format}, width: {img.width}, height: {img.height}"
        )

        current_app.logger.info("Generating composed image")
        
        img_res = algo.build(img)
        img_res_base64 = image_to_base64(img_res)

        response = {
            "message": "OK",
            "shape": [img_res.width, img_res.height],
            "image": img_res_base64.decode(),       
        }

        return response, HTTPStatus.OK