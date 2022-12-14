import unittest
from unittest.mock import patch, MagicMock
from get_book_titles import getBookTitles
from client.inventory_client import InventoryClient

# instantiate the client to be used in the test to avoid repeating the same code
cli = InventoryClient()
mock_client = MagicMock()
mock_client.get_book.side_effect = [MagicMock(title="The Hitchhiker's Guide to the Galaxy"),
                                    MagicMock(title="The Great Gatsby")]


class Test(unittest.TestCase):
    # test get_book_titles using mock object as a client API accessor
    def testGetBookTitlesMock1(self, mock=mock_client):
        self.assertEqual(getBookTitles(["0001", "0003"], mock),
                         ["The Hitchhiker's Guide to the Galaxy",
                          "The Great Gatsby"])

    # test get_book_titles patching the dependency function (get_book)
    @patch('client.inventory_client.InventoryClient.get_book')
    def testGetBookTitlesMock2(self, mock_get_book):
        mock_get_book.return_value = MagicMock(title="Becoming")

        self.assertEqual(getBookTitles(["0002"], cli), ["Becoming"])

    # test get_book_titles using a live server to access the API
    def testGetBookTitlesLive(self):
        self.assertEqual(getBookTitles(["0001", "0003"], cli), ["The Hitchhiker's Guide to the Galaxy",
                                                                "The Great Gatsby"])
