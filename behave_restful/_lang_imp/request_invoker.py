from requests_toolbelt.multipart.encoder import MultipartEncoder

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
    files = _get_files(context)

    if files is not None:
        fields = {
            name: (val[0], open(val[1], 'rb'), val[2]) for name, val in files.items()
        }

        if params is not None:
            for name, val in params.items():
                fields[name] = val
        
        multipart_data = MultipartEncoder(fields=fields)

        context.response = context.session.post(
            context.request_url,
            data=multipart_data,
            headers={ 'Content-Type': multipart_data.content_type }
        )

    else:
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


def _get_files(context):
    return context.request_files if hasattr(context, 'request_files') else None