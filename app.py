from flask import Flask
from calculator.routes import bp


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["HISTORY_FILE"] = "history.json"
    if config:
        app.config.update(config)
    app.register_blueprint(bp)
    return app


app = create_app()
