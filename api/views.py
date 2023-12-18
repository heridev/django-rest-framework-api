from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ItemSerializer
from base.models import Item


@api_view(['GET'])
def get_data(request):
    items = Item.objects.all()
    serializedData = ItemSerializer(items, many=True)
    return Response(serializedData.data)


@api_view(['POST'])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
