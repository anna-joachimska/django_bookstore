from .models import Book
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework import status

class BooksView(generics.GenericAPIView):

    serializer_class = BookSerializer

    def get(self, request):
        books = Book.objects.all().values()
        total_books = books.count()
        return Response({"status":status.HTTP_200_OK, "total": total_books, "data": books,})

    def get_book(self, name):
        try:
            return Book.objects.get(name=name)
        except:
            return None

    def post(self, request):
        if not (request.data):
            raise serializers.ValidationError({"message": "You must pass a data to create a Book"})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "book": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        book = self.get_book(pk=pk)
        if book == None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(book)
        return Response({"status": "success", "book": serializer.data})

    def patch(self, request, pk):
        book = self.get_book(pk)
        if book == None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "book": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_book(pk)
        if book == None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookBookstore(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        book = self.get_book(pk=pk)
        if book == None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(book)
        return Response({"status": "success", "bookstore": serializer.data})


    def post(self, request, pk):
        book = self.get_book(pk)
        if book == None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            book, data=request.data, partial=True)

        for i in range(0, len(request.data['bookstores'])):
            if book.bookstores.filter(pk=request.data['bookstores'][i]).exists():

                return Response({"status": "fail", "message": "this bookstore already is in this book"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                book.bookstores.add(request.data['bookstores'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "bookstore added succesfully", "book": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_book(pk)
        if book == None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            book, data=request.data, partial=True)

        for i in range(0, len(request.data['bookstores'])):
            if not book.bookstores.filter(pk=request.data['bookstores'][i]).exists():
                return Response({"status": "fail", "message": "this bookstore isn't in this book"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                book.bookstores.remove(request.data['bookstores'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "bookstore deleted succesfully", "book": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
