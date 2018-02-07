"""
"""
import json

def set_url(context, url):
    """
    """
    resolved_url = context.vars.resolve(url)
    context.request_url = resolved_url


def set_json_payload(context, payload):
    """
    """
    resolved_payload = context.vars.resolve(payload)
    context.request_json_payload = json.loads(resolved_payload)
