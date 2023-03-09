from .models import Book
from .serializers import BookSerializer, AddBookstoreToBookSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status


class BooksView(generics.GenericAPIView):
    serializer_class = BookSerializer

    def get(self, request):
        books = Book.objects.all().values()
        total_books = books.count()
        return Response({"status": status.HTTP_200_OK, "total": total_books, "data": books, })

    def post(self, request):
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
        if book is None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(book)
        return Response({"status": "success", "book": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        book = self.get_book(pk)
        if book is None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(book, data=request.data, partial=True)
        if 'bookstores' in request.data.keys():
            new_bookstore_list = []
            old_bookstore_list = []
            for bookstore in request.data['bookstores']:
                if book.bookstores.filter(pk=bookstore).exists():
                    old_bookstore_list.append(bookstore)
                else:
                    new_bookstore_list.append(bookstore)
            if len(old_bookstore_list) > 0:
                return Response({"status": "fail", "message": "this books already is in this bookstores",
                                 "bookstores": old_bookstore_list},
                                status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "book": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_book(pk)
        if book is None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response({"status": "success", "message": "book deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class AddOrRemoveBookstoreFromBook(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = AddBookstoreToBookSerializer

    def get_book(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        book = self.get_book(pk=pk)
        if book is None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(book)
        return Response({"status": "success", "book": serializer.data})

    def post(self, request, pk):
        book = self.get_book(pk)
        if book is None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(book, data=request.data, partial=True)
        if serializer.is_valid():

            new_bookstore_list = []
            old_bookstore_list = []
            for bookstore in request.data['bookstores']:
                if book.bookstores.filter(pk=bookstore).exists():
                    old_bookstore_list.append(bookstore)
                else:
                    new_bookstore_list.append(bookstore)
            if len(old_bookstore_list) > 0:
                return Response({"status": "fail", "message": "this books already is in this bookstores",
                                 "bookstores": old_bookstore_list},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for bookstore in new_bookstore_list:
                    book.bookstores.add(bookstore)

            return Response(
                {"status": "success", "message": "bookstore added successfully", "book": serializer.data})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_book(pk)
        if book is None:
            return Response({"status": "fail", "message": f"Book with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            book, data=request.data, partial=True)

        if serializer.is_valid():
            new_bookstore_list = []
            old_bookstore_list = []
            for bookstore in request.data['bookstores']:
                if not book.bookstores.filter(pk=bookstore).exists():
                    new_bookstore_list.append(bookstore)
                else:
                    old_bookstore_list.append(bookstore)

            if len(new_bookstore_list) > 0:
                return Response({"status": "fail", "message": "this book isn't in this bookstores",
                                 "bookstores_to_remove": new_bookstore_list, "existing_bookstores": old_bookstore_list},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for bookstore in old_bookstore_list:
                    book.bookstores.remove(bookstore)

            return Response(
                {"status": "success", "message": "bookstore deleted successfully", "book": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
