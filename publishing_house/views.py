from .models import PublishingHouse
from .serializers import PublishingHouseSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from book.models import Book


class PublishingHousesView(generics.GenericAPIView):
    serializer_class = PublishingHouseSerializer

    def get(self, request):
        publishing_houses = PublishingHouse.objects.all().values()
        total_publishing_houses = publishing_houses.count()
        return Response({
            "status": status.HTTP_200_OK,
            "total": total_publishing_houses,
            "data": publishing_houses,
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "publishing_house": serializer.data}, status=status.HTTP_201_CREATED)
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
        if publishing_house is None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(publishing_house)
        return Response({"status": "success", "publishing_house": serializer.data})

    def patch(self, request, pk):
        publishing_house = self.get_publishing_house(pk)
        if publishing_house is None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(publishing_house, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "publishing_house": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publishing_house = self.get_publishing_house(pk)

        if publishing_house is None:
            return Response({"status": "fail", "message": f"Publishing House with id: {pk} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if len(Book.objects.filter(publishing_house=pk)) > 0:
            return Response({"status": "fail", "message": 'you cannot delete publishing house with books in it'},
                            status=status.HTTP_400_BAD_REQUEST)

        publishing_house.delete()
        return Response({"status": "success", "message": "publishing house deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
