import os

from flask import send_from_directory

from api.app import create_app


settings_module = os.getenv("APP_SETTINGS_MODULE")
app = create_app(settings_module)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")