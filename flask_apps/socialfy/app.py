from flask import Flask
import tekore as tk
from decouple import config
import logging
import shutil


def app_factory() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')

    from blueprints.api_bp import api
    app.register_blueprint(api)

    from blueprints.auth_bp import auth
    app.register_blueprint(auth)

    from blueprints.main_bp import main
    app.register_blueprint(main)

    # Patch Tekore
    try:
        shutil.copy(config('PATCH_SRC'), config('PATCH_DIR'))
    except:
        logging.info("Tekore has allready been patched")

    return app


if __name__ == '__main__':
    application = app_factory()
    application.run('0.0.0.0', 5000, threaded=True)
