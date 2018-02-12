"""
"""

def send_get(context):
    """
    """
    params = _get_params(context)
    context.response = context.session.get(
        context.request_url,
        params=params
    )


def send_post(context):
    """
    """
    params = _get_params(context)
    context.response = context.session.post(
        context.request_url,
        params=params,
        json=context.request_json_payload
    )


def send_put(context):
    """
    """
    params = _get_params(context)
    context.response = context.session.put(
        context.request_url,
        params=params,
        json=context.request_json_payload
    )


def send_delete(context):
    """
    """
    params = _get_params(context)
    context.response = context.session.delete(
        context.request_url,
        params=params
    )



def _get_params(context):
    return context.request_params if hasattr(context, 'request_params') else None