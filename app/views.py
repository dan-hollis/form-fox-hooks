import json
import re

import requests
from flask import Blueprint, current_app, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.logging_utils import get_logger, log_request_data

discord_ff = Blueprint('discord-ff', __name__)

logger = get_logger(__name__)


@discord_ff.route('/discord-ff-events', methods=['POST', 'GET'])
def events():
    if request.method == 'GET':
        return '', 200

    try:
        data = request.json

        if data is None:
            current_app.logger.warning('Received request with no JSON data')
            return '', 400

        log_request_data(logger, json.dumps(data, indent=4), 'discord-ff-events')

        usernames = []
        if data['response']['form']['hid'] == current_app.config['FF_FORM_ID']:
            is_guildie = data['response']['answers'][0] == 'Yes'
            user_id = data['response']['user_id']

            if is_guildie:
                raider_role_id = current_app.config['RAIDER_ROLE_ID']
            else:
                raider_role_id = current_app.config['PUG_RAIDER_ROLE_ID']
                usernames_raw = data['response']['answers'][0]
                # Split on common separators: comma, newline, pipe, semicolon, tab
                usernames = [
                    username.strip()
                    for username in re.split(r'[,\n|;\t]+', usernames_raw)
                    if username.strip()
                ]
                current_app.logger.info('PUG Raider usernames: %s', usernames)
                if not usernames:
                    current_app.logger.warning(
                        'No usernames in PUG Raider request: %s', usernames_raw
                    )
                else:
                    docs_service = build(
                        'docs', 'v1', credentials=current_app.config['GOOGLE_CREDS']
                    )
                    try:
                        docs_service.documents().batchUpdate(
                            documentId=current_app.config['GOOGLE_DOC_ID'],
                            body={
                                'requests': [
                                    {
                                        'insertText': {
                                            'text': f'{"\n".join(usernames)}',
                                            'endOfSegmentLocation': {},
                                        }
                                    }
                                ]
                            },
                        ).execute()
                    except HttpError:
                        current_app.logger.exception(
                            'Failed to update Google Docs form with PUG Raider names'
                        )

            server_id = current_app.config['DISCORD_SERVER_ID']
            url_endpoint = f'https://discord.com/api/guilds/{server_id}/members/{user_id}/roles/{raider_role_id}'
            discord_headers = {
                'Authorization': f'Bot {current_app.config["DISCORD_BOT_TOKEN"]}'
            }
            role_request = requests.put(
                url_endpoint, headers=discord_headers, timeout=60
            )
            if role_request.status_code != 204:  # noqa: PLR2004
                current_app.logger.warning(
                    'Failed to add user role %s to %s: %s',
                    raider_role_id,
                    user_id,
                    role_request,
                )

        current_app.logger.info('Successfully processed Discord FF event')

    except Exception:
        current_app.logger.exception('Error processing Discord FF event: %s')
        return '', 500

    else:
        return '', 200
