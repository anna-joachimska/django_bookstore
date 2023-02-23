from .models import PublishingHouse
from .serializers import PublishingHouseSerializer
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework import status

class PublishingHousesView(generics.GenericAPIView):

    serializer_class = PublishingHouseSerializer

    def get(self, request):
        publishing_houses = PublishingHouse.objects.all().values()
        total_publishing_houses = publishing_houses.count()
        return Response({
                "status":status.HTTP_200_OK,
                "total": total_publishing_houses,
                "data": publishing_houses,
        })

    def post(self, request):
        if not (request.data):
            raise serializers.ValidationError({"message": "You must pass a data to create a Publishing House"})

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "publishing house": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PublishingHouseDetail(generics.GenericAPIView):
    queryset = PublishingHouse.objects.all()
    serializer_class = PublishingHouseSerializer

    def get_publishing_house(self, pk):
        try:
            return PublishingHouse.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        publishing_house = self.get_publishing_house(pk=pk)
        if publishing_house == None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(publishing_house)
        return Response({"status": "success", "publishing house": serializer.data})

    def patch(self, request, pk):
        publishing_house = self.get_publishing_house(pk)
        if publishing_house == None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            publishing_house, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "publishing house": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publishing_house = self.get_publishing_house(pk)
        serializer = self.serializer_class(publishing_house)
        if publishing_house == None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if len(serializer.data['books']) > 0:
            return Response({"status": "fail", "message": 'you cannot delete publishing house with books in it'},
                            status=status.HTTP_400_BAD_REQUEST)

        publishing_house.delete()
        return Response({"status": "success", "message": "publishing house deleted succesfully"},status=status.HTTP_204_NO_CONTENT)

class PublishingHouseBooks(generics.GenericAPIView):
    queryset = PublishingHouse.objects.all()
    serializer_class = PublishingHouseSerializer


    def get_publishing_house(self, pk):
        try:
            return PublishingHouse.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        publishing_house = self.get_publishing_house(pk=pk)
        if publishing_house == None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(publishing_house)
        return Response({"status": "success", "publishing house": serializer.data})


    def post(self, request, pk):
        publishing_house = self.get_publishing_house(pk)
        if publishing_house == None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            publishing_house, data=request.data, partial=True)

        for i in range(0, len(request.data['books'])):
            if publishing_house.books.filter(pk=request.data['books'][i]).exists():

                return Response({"status": "fail", "message": "this book already is in this publishing house"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                publishing_house.books.add(request.data['books'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "book added succesfully", "publishing house": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publishing_house = self.get_publishing_house(pk)
        if publishing_house == None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            publishing_house, data=request.data, partial=True)

        for i in range(0, len(request.data['books'])):
            if not publishing_house.books.filter(pk=request.data['books'][i]).exists():
                return Response({"status": "fail", "message": "this book isn't in this publishing house"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                publishing_house.books.remove(request.data['books'][i])
        if serializer.is_valid():
            return Response(
                {"status": "success", "message": "books deleted succesfully", "publishing house": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
