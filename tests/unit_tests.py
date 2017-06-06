import unittest
import mock

from app.api.items import ReqItem
from app.errors import InvalidParameterError


class ReqItemTest(unittest.TestCase):

    def test_InvalidParameterError_external_id(self):

        req = mock.Mock()
        req.context = {'data': {}}

        resp = mock.Mock()

        req_item = ReqItem()

        with self.assertRaises(InvalidParameterError) as err:
            req_item.on_post(req, resp)

        data = err.exception.error['description']['external_id'][0]
        self.assertEqual(data, 'required field')

    @mock.patch('uuid.uuid4', lambda: "aaaaaaaa-aaaa-aaaa-0000-aaaaaaaaaaa")
    @mock.patch('app.api.update_db.add_new_cart.delay', lambda x: None)
    @mock.patch('app.api.update_db.update_item.delay', lambda x: None)
    def test_InvalidParameterError(self):

        mock_uid = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa'
        mock_lambda_uid = "aaaaaaaa-aaaa-aaaa-0000-aaaaaaaaaaa"

        req = mock.Mock()
        req.context = {'data': {'external_id': mock_uid}}

        redis_mock = mock.Mock()
        resp = mock.Mock()

        req_item = ReqItem()
        req_item.r = redis_mock

        req_item.on_post(req, resp)
        resp.set_cookie.assert_called_with('cart_id', mock_lambda_uid)


if __name__ == '__main__':
    unittest.main()
