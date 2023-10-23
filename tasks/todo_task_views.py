from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from tasks.models import  todo

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter




from commons.pagination import Pagination
from tasks.serializers import TodoSerializer




# Create your views here.

@extend_schema(
    parameters=[
        OpenApiParameter("page"),
        OpenApiParameter("size"),
  ],
    request=TodoSerializer,
    responses=TodoSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([AuthPermEnum.DESIGNATION_LIST.name])
def getAlltodo(request):
    todos = todo.objects.all()
    total_elements = todos.count()

    page = request.query_params.get('page')
    size = request.query_params.get('size')

    # Pagination
    pagination = Pagination()
    pagination.page = page
    pagination.size = size
    todos = pagination.paginate_data(todos)

    serializer = TodoSerializer(todos, many=True)

    response = {
        'todos': serializer.data,
        'page': pagination.page,
        'size': pagination.size,
        'total_pages': pagination.total_pages,
        'total_elements': total_elements,
    }

    return Response(response, status=status.HTTP_200_OK)


@extend_schema(
    request=TodoSerializer,
    responses=TodoSerializer
)
@api_view(['GET'])
def getAlltodoWithoutPagination(request):
    todos = todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    response = {
        'todos': serializer.data,
    }
    return Response(response, status=status.HTTP_200_OK)


@extend_schema(request=TodoSerializer, responses=TodoSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([SiteSettingPermEnum.GENERAL_SETTING_UPDATE.name])
def getAtodo(request, pk):
    try:
        todos = todo.objects.get(pk=pk)
        serializer = TodoSerializer(todos)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"todos id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)





@extend_schema(request=TodoSerializer, responses=TodoSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def createtodo(request):
    data = request.data
    filtered_data = {}
    
    for key, value in data.items():
        if value != '' and value != '0':
            filtered_data[key] = value
        
   
    serializer = TodoSerializer(data=filtered_data)
    if serializer.is_valid():
        serializer.save()
      
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=TodoSerializer, responses=TodoSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def updatetodo(request,pk):
    try:
        bus_booking = todo.objects.get(pk=pk)
        data = request.data
     
      
        
        serializer = TodoSerializer(bus_booking, data=data)
        if serializer.is_valid():
            serializer.save()
         
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({'detail': f"todos id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(request=TodoSerializer, responses=TodoSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def deletetodo(request, pk):
    try:
        todos = todo.objects.get(pk=pk)
        todos.delete()
      
        return Response({'detail': f'todos  id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail': f"todos  id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


