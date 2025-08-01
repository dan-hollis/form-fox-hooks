import logging
import logging.handlers
from pathlib import Path

import yaml
from flask import Flask
from google.auth import default

from app.views import discord_ff


def setup_logging(app: Flask):
    """Configure logging for the Flask application"""
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    root_logger = logging.getLogger()

    if root_logger.handlers:
        app.logger.setLevel(logging.INFO)
        return app

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # App logger
    app_log_file = log_dir / 'app.log'
    app_handler = logging.handlers.RotatingFileHandler(
        app_log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.DEBUG)

    root_logger.addHandler(app_handler)
    root_logger.setLevel(logging.INFO)

    # Set Flask app logger level but don't add handlers
    app.logger.setLevel(logging.INFO)

    return app


config_file_path = Path(__file__).parent / 'config.yml'
config = yaml.safe_load(config_file_path.read_text(encoding='utf-8'))

creds, _ = default(scopes=config['google']['scopes'])

app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask']['secret_key']
app.config['GOOGLE_CREDS'] = creds
app.config['GOOGLE_DOC_ID'] = config['google']['doc_id']
app.config['FF_FORM_ID'] = config['form_fox']['form_id']
app.config['DISCORD_SERVER_ID'] = config['discord']['server_id']
app.config['RAIDER_ROLE_ID'] = config['discord']['raider_role_id']
app.config['PUG_RAIDER_ROLE_ID'] = config['discord']['pug_raider_role_id']
app.config['DISCORD_BOT_TOKEN'] = config['discord']['bot_token']

app = setup_logging(app)

app.register_blueprint(discord_ff)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
