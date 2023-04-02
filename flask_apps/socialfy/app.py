from flask import Flask
import tekore as tk 
from decouple import config

spotify = tk.Spotify()


def app_factory() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    
    from blueprints.api_bp import api
    app.register_blueprint(api)

    from blueprints.auth_bp import auth
    app.register_blueprint(auth)


    from blueprints.main_bp import main
    app.register_blueprint(main)
     
    
    return app

if __name__ == '__main__':
    application = app_factory()
    application.run('127.0.0.1', 5000)