import unittest

from assertpy import assert_that

import behave_restful._lang_imp.request_invoker as _invoker



class TestRequestInvokerInterface(unittest.TestCase):

    def setUp(self):
        super(TestRequestInvokerInterface, self).setUp()
        self.response = ResponseDouble()
        self.session = SessionDouble()
        self.session.response = self.response
        self.context = ContextDouble()
        self.context.session = self.session
        self.context.request_url = 'http://my.server.com/resource'
        self.context.request_json_payload = {
            'id': 12,
            'name': 'a name'
        }
        self.context.request_params = {'foo': 56,
                                       'bar': 'baz'}


    # send_get()
    def test_invokes_get_on_session(self):
        _invoker.send_get(self.context)
        assert_that(self.session.get_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)


    def test_get_stores_response_in_context(self):
        _invoker.send_get(self.context)
        assert_that(self.context.response).is_same_as(self.response)


    def test_get_request_includes_params(self):
        _invoker.send_get(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)



    # send_post()
    def test_invokes_post_on_session(self):
        _invoker.send_post(self.context)
        assert_that(self.session.post_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)


    def test_invokes_post_with_json_payload(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_json).is_equal_to(self.context.request_json_payload)


    def test_post_stores_response_in_context(self):
        _invoker.send_post(self.context)
        assert_that(self.context.response).is_same_as(self.response)


    def test_post_request_includes_params(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)


    # send_put()
    def test_invokes_put_on_session(self):
        _invoker.send_put(self.context)
        assert_that(self.session.put_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)


    def test_invokes_put_with_json_payload(self):
        _invoker.send_put(self.context)
        expected_payload = self.session.request_kwargs.get('json')
        assert_that(expected_payload).is_equal_to(self.context.request_json_payload)


    def test_put_stores_response_in_context(self):
        _invoker.send_put(self.context)
        assert_that(self.context.response).is_same_as(self.response)


    def test_put_request_includes_params(self):
        _invoker.send_put(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)


    # send_patch()
    def test_invokes_patch_on_session(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.patch_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)


    def test_invokes_patch_with_json_payload(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.request_json).is_equal_to(self.context.request_json_payload)


    def test_patch_request_includes_params(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)


    def test_patch_stores_response_in_context(self):
        _invoker.send_patch(self.context)
        assert_that(self.context.response).is_same_as(self.response)



    # send_delete()
    def test_invokes_delete_on_session(self):
        _invoker.send_delete(self.context)
        assert_that(self.session.delete_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)


    def test_delete_stores_response_in_context(self):
        _invoker.send_delete(self.context)
        assert_that(self.context.response).is_same_as(self.response)


    def test_delete_request_includes_params(self):
        _invoker.send_delete(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)
        
        



class SessionDouble(object):
    def __init__(self):
        self.response = None
        self.get_invoked = False
        self.post_invoked = False
        self.put_invoked = False
        self.patch_invoked = False
        self.delete_invoked = False
        self.request_url = None
        self.request_params = None
        self.request_data = None
        self.request_json = None
        self.request_kwargs = None


    def get(self, url, params=None, **kwargs):
        self.get_invoked = True
        self.request_url = url
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


    def post(self, url, data=None, json=None, params=None, **kwargs):
        self.post_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_json = json
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


    def put(self, url, data=None, params=None, **kwargs):
        self.put_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


    def patch(self, url, data=None, json=None, params=None, **kwargs):
        self.patch_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_json = json
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


    def delete(self, url, params=None, **kwargs):
        self.delete_invoked = True
        self.request_url = url
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response



class ResponseDouble(object):
    pass



class ContextDouble(object):
    pass



if __name__=="__main__":
    unittest.main()