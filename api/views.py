from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    person = {'name': 'heriberto', 'phone_number': '312123xxxx'}
    return Response(person)
