import grpc
from service import library_pb2_grpc, library_pb2


class InventoryClient:
    def __init__(self, host="localhost", port=50051):
        address = f"{host}:{port}"
        self.channel = grpc.insecure_channel(address)
        self.stub = library_pb2_grpc.InventoryServiceStub(self.channel)

    def get_book(self, isbn):
        try:
            # try RPC call to get the book and return the book
            response = self.stub.GetBook(library_pb2.GetBookRequest(isbn=isbn))
            return response.book
        except grpc.RpcError as e:
            print(e.details())
            return None

    def create_book(self, book):
        try:
            # try RPC call to create the book and return success or not
            response = self.stub.CreateBook(library_pb2.CreateBookRequest(book=book))
            return response.success
        except grpc.RpcError as e:
            print(e.details())
            return False
