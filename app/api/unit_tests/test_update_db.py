from __future__ import absolute_import

import unittest

from mock import mock
from app.api.update_db import add_new_cart, update_item


class UpdateDbTest(unittest.TestCase):

    def test_add_new_cart(self):
        session = mock.Mock()
        data = {'cart_id': 1337}

        add_new_cart(data, session)

        session.commit.assert_called_once()
        session.add.assert_called_once()

        self.assertEqual(session.mock_calls[0][1][0].id, data['cart_id'])

    def test_update_item(self):
        session = mock.Mock()
        session.query.filter_by = 3

        data = {'cart_id': 1337, 'name': 'Test_1',
                'value': 42, 'external_id': 1234}

        update_item(data, session)

        session.commit.assert_called_once()

        self.assertEqual(session.mock_calls[1][2]['cart_id'], 1337)
        self.assertEqual(session.mock_calls[1][2]['external_id'], 1234)


if __name__ == '__main__':
    unittest.main()
