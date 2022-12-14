import logging
from typing import List
from client import inventory_client


def getBookTitles(isbn_list: List[str], client: inventory_client.InventoryClient) -> List[str]:
    """Get book titles from the server.

    Args:
        isbn_list: A list of ISBNs.
        client: The gRPC client.

    Returns:
        A list of book titles.
    """
    retList = []
    for isbn in isbn_list:
        book = client.get_book(isbn)
        if book:
            logging.info("Book found: %s", book)
            retList.append(book.title)
        else:
            retList.append("Book not found")

    return retList


if __name__ == '__main__':
    client = inventory_client.InventoryClient()
    print(getBookTitles(["0001", "0003"], client))
