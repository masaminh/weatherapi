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

    code = event['pathParameters']['code']

    result = logic.get_hourly(code)
    response = _get_apigateway_response(result)
    return response


def _get_apigateway_response(obj):
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(obj, ensure_ascii=False)
    }

    return response
