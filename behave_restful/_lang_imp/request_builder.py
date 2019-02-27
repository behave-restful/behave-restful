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


def set_request_params(context, params):
    """
    """
    resolve = context.vars.resolve
    resolved_params = {resolve(param['param']): resolve(param['value']) for param in params}
    context.request_params = resolved_params

def set_file_payload(context, params):
    """
    """
    resolve = context.vars.resolve

    # request_files will be a dict of param=>(filename, fileobj, content_type)
    resolved_files = {
        resolve(param['param']): (
            resolve(param['filename']), 
            resolve(param['file']),
            resolve(param['content_type'])
        ) for param in params
    }

    context.request_files = resolved_files