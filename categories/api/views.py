from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from categories import models


@api_view(["GET"])
def category_list_api(request):
    categories = models.Category.objects.all()
    serializer = serializers.CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def category_create_api(request):
    serializer = serializers.CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT", "POST"])
def category_edit_api(request, id):
    try:
        category = models.Category.objects.get(id=id)
    except models.Category.DoesNotExist:
        return Response({"id": f"Category with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def category_detail_api(request, id):
    try:
        category = models.Category.objects.get(id=id)
    except models.Category.DoesNotExist:
        return Response({"id": f"Category with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = serializers.CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE", "POST"])
def category_delete_api(request, id):
    try:
        category = models.Category.objects.get(id=id)
    except models.Category.DoesNotExist:
        return Response({"id": f"Category with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response({}, status=status.HTTP_204_NO_CONTENT)
