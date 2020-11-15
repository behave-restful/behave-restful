"""
"""

def send_get(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.get(
        context.request_url,
        headers=headers,
        params=params
    )


def send_post(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.post(
        context.request_url,
        headers=headers,
        params=params,
        json=context.request_json_payload
    )


def send_put(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.put(
        context.request_url,
        headers=headers,
        params=params,
        json=context.request_json_payload
    )


def send_patch(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.patch(
        context.request_url,
        headers=headers,
        params=params,
        json=context.request_json_payload
    )


def send_delete(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.delete(
        context.request_url,
        headers=headers,
        params=params
    )



def _get_params(context):
    return context.request_params if hasattr(context, 'request_params') else None

def _get_request_headers(context):
    return context.request_headers if hasattr(context, 'request_headers') else None
