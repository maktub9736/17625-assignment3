import logging
from concurrent import futures

import grpc
from service import library_pb2_grpc, library_pb2


class LibraryServicer(library_pb2_grpc.InventoryServiceServicer):
    def __init__(self, *args, **kwargs):
        # Initialize the books dictionary，key is isbn, value is book, stored in memory
        b1 = {"isbn": "0001",
              "title": "The Hitchhiker's Guide to the Galaxy",
              "author": "Douglas Adams",
              "genre": 1,
              "publish_year": 1979}
        b2 = {"isbn": "0002",
              "title": "Becoming",
              "author": "Michelle Obama",
              "genre": 3,
              "publish_year": 2018}
        b3 = {"isbn": "0003",
              "title": "The Great Gatsby",
              "author": "F. Scott Fitzgerald",
              "genre": 4,
              "publish_year": 1925}
        self.books = dict({"0001": b1, "0002": b2, "0003": b3})

    def GetBook(self, request, context):
        isbn = request.isbn
        logging.info("isbn: %s", isbn)
        if request.isbn in self.books:
            b = self.books[request.isbn]

            return library_pb2.GetBookResponse(book=b)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return library_pb2.GetBookResponse()

    def CreateBook(self, request, context):
        if request.book.isbn in self.books:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Book already exists")
            return library_pb2.CreateBookResponse(success=False)
        else:
            self.books[request.book.isbn] = request.book
            return library_pb2.CreateBookResponse(success=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_InventoryServiceServicer_to_server(LibraryServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
