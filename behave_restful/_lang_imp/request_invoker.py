"""
"""

def send_get(context):
    """
    """
    context.response = context.session.get(context.request_url)


def send_post(context):
    """
    """
    context.response = context.session.post(
        context.request_url,
        json=context.request_json_payload
    )


def send_put(context):
    """
    """
    context.response = context.session.put(
        context.request_url,
        json=context.request_json_payload
    )


def send_delete(context):
    """
    """
    context.response = context.session.delete(
        context.request_url
    )