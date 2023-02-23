from .models import Bookstore
from .serializers import BookstoreSerializer
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework import status

class BookstoresView(generics.GenericAPIView):

    serializer_class = BookstoreSerializer

    def get(self, request):
        bookstores = Bookstore.objects.all().values()
        total_bookstores = bookstores.count()
        return Response({
                "status":status.HTTP_200_OK,
                "total": total_bookstores,
                "data": bookstores,
        })

    def post(self, request):
        if not (request.data):
            raise serializers.ValidationError({"message": "You must pass a data to create a Bookstore"})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "bookstore": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BookstoreDetail(generics.GenericAPIView):
    queryset = Bookstore.objects.all()
    serializer_class = BookstoreSerializer

    def get_bookstore(self, pk):
        try:
            return Bookstore.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        bookstore = self.get_bookstore(pk=pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore)
        return Response({"status": "success", "bookstore": serializer.data})

    def patch(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            bookstore, data=request.data, partial=True)
        if bookstore.books.filter(pk=request.data['books'][0]).exists():
            return Response({"status": "fail", "message": "this book already is in this bookstore"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif bookstore.publishing_houses.filter(pk=request.data['publishing_houses'][0]).exists():
            return Response({"status": "fail", "message": "this publishing house already is in this bookstore"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "bookstore": serializer.data})
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        bookstore.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookstoreBooks(generics.GenericAPIView):
    queryset = Bookstore.objects.all()
    serializer_class = BookstoreSerializer


    def get_bookstore(self, pk):
        try:
            return Bookstore.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        bookstore = self.get_bookstore(pk=pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore)
        return Response({"status": "success", "bookstore": serializer.data})


    def post(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            bookstore, data=request.data, partial=True)

        for i in range(0, len(request.data['books'])):
            if bookstore.books.filter(pk=request.data['books'][i]).exists():

                return Response({"status": "fail", "message": "this book already is in this bookstore"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                bookstore.books.add(request.data['books'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "book added succesfully", "bookstore": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            bookstore, data=request.data, partial=True)

        for i in range(0, len(request.data['books'])):
            if not bookstore.books.filter(pk=request.data['books'][i]).exists():
                return Response({"status": "fail", "message": "this book isn't in this bookstore"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                bookstore.books.remove(request.data['books'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "books deleted succesfully", "bookstore": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BookstorePublishingHouses(generics.GenericAPIView):
    queryset = Bookstore.objects.all()
    serializer_class = BookstoreSerializer

    def get_bookstore(self, pk):
        try:
            return Bookstore.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        bookstore = self.get_bookstore(pk=pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore)
        return Response({"status": "success", "bookstore": serializer.data})


    def post(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            bookstore, data=request.data, partial=True)

        for i in range(0, len(request.data['publishing_houses'])):
            if bookstore.publishing_houses.filter(pk=request.data['publishing_houses'][i]).exists():

                return Response({"status": "fail", "message": "this book already is in this bookstore"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                bookstore.publishing_houses.add(request.data['publishing_houses'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "publishing house added succesfully", "bookstore": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore == None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            bookstore, data=request.data, partial=True)

        for i in range(0, len(request.data['publishing_houses'])):
            if not bookstore.publishing_houses.filter(pk=request.data['publishing_houses'][i]).exists():
                return Response({"status": "fail", "message": "this publishing house isn't in this bookstore"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                bookstore.publishing_house.remove(request.data['publishing_house'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "publishing house deleted succesfully", "bookstore": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
