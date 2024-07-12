from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    # Lire les variables d'environnement pour configurer Flask
    app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

    from .routes import main
    app.register_blueprint(main)

    # Configuration des logs
    if app.debug:
        import logging
        from logging import StreamHandler
        handler = StreamHandler()
        handler.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)

    return app
