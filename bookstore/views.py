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
            "status": status.HTTP_200_OK,
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
        if bookstore is None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore)
        return Response({"status": "success", "bookstore": serializer.data})

    def patch(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore is None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore, data=request.data, partial=True)
        try:
            for publishing_house in request.data['publishing_houses']:
                if bookstore.publishing_houses.filter(pk=publishing_house).exists():
                    return Response({"status": "fail", "message": "this publishing house already is in this bookstore"},
                                    status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "bookstore": serializer.data})
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "bookstore": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore is None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        bookstore.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddOrDeletePublishingHouseFromBookstore(generics.GenericAPIView):
    queryset = Bookstore.objects.all()
    serializer_class = BookstoreSerializer

    def get_bookstore(self, pk):
        try:
            return Bookstore.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        bookstore = self.get_bookstore(pk=pk)
        if bookstore is None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore)
        return Response({"status": "success", "bookstore": serializer.data})

    def post(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore is None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore, data=request.data, partial=True)

        if serializer.is_valid():

            new_publishing_houses_list = []
            old_publishing_houses_list = []
            for publishing_house in request.data['publishing_houses']:
                if bookstore.publishing_houses.filter(pk=publishing_house).exists():
                    old_publishing_houses_list.append(publishing_house)
                else:
                    new_publishing_houses_list.append(publishing_house)
            if len(old_publishing_houses_list) > 0:
                return Response({"status": "fail", "message": "this publishing house already is in this bookstore"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for publishing_house in new_publishing_houses_list:
                    bookstore.publishing_houses.add(publishing_house)

            return Response(
                {"status": "success", "message": "publishing house added succesfully", "bookstore": serializer.data})

        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bookstore = self.get_bookstore(pk)
        if bookstore is None:
            return Response({"status": "fail", "message": f"Bookstore with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(bookstore, data=request.data, partial=True)

        if serializer.is_valid():
            new_publishing_house_list = []
            old_publishing_house_list = []
            for publishing_house in request.data['publishing_houses']:
                if not bookstore.publishing_houses.filter(pk=publishing_house).exists():
                    old_publishing_house_list.append(publishing_house)
                else:
                    new_publishing_house_list.append(publishing_house)

            if len(old_publishing_house_list) > 0:
                return Response({"status": "fail", "message": "this publishing house isn't in this bookstore"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                for publishing_house in new_publishing_house_list:
                    bookstore.publishing_houses.remove(publishing_house)

            return Response(
                {"status": "success", "message": "publishing house deleted succesfully", "bookstore": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
