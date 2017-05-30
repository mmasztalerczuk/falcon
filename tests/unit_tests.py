import unittest
import mock
from redis import ConnectionError

from app.api.items import ReqItem
from app.errors import InvalidParameterError


class ReqItemTest(unittest.TestCase):

    def test_InvalidParameterError_external_id(self):

        req = mock.Mock()
        req.context = { 'data' : { }}

        resp = mock.Mock()

        reqItem = ReqItem()

        with self.assertRaises(InvalidParameterError) as err:
            reqItem.on_post(req, resp)

        self.assertTrue(err.exception.error['description']['external_id'][0] == 'required field')

    @mock.patch('uuid.uuid4', lambda : "aaaaaaaa-aaaa-aaaa-0000-aaaaaaaaaaa")
    @mock.patch('app.api.update_db.add_new_cart.delay', lambda x: None)
    @mock.patch('app.api.update_db.update_item.delay', lambda x: None)
    def test_InvalidParameterError(self):

        req = mock.Mock()
        req.context = { 'data' : { 'external_id' : 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa'}}

        redisMock = mock.Mock()
        resp = mock.Mock()

        reqItem = ReqItem()
        reqItem.r = redisMock

        reqItem.on_post(req, resp)
        resp.set_cookie.assert_called_with('cart_id', "aaaaaaaa-aaaa-aaaa-0000-aaaaaaaaaaa")


if __name__ == '__main__':
    unittest.main()