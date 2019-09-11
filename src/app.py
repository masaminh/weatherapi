"""weatherapi API部."""
import json
import logging

from aws_xray_sdk.core import patch_all

import logic

patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hourly_handler(event, context):
    """GET /hourly.

    Arguments:
        event {dict} -- イベント情報
        context {object} -- コンテキスト

    Returns:
        str -- json文字列

    """
    del context

    if 'pathParameters' not in event:
        return _get_apigateway_response(None, 400, 'Bad Request')

    code = event['pathParameters']['code']

    result = logic.get_hourly(code)
    response = _get_apigateway_response(result)
    return response


def _get_apigateway_response(obj, statusCode=200, message='OK'):
    body = obj.copy() if obj else dict()
    body['message'] = message
    response = {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body, ensure_ascii=False)
    }

    return response
