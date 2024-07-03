from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from .models import student
from rest_framework.pagination import PageNumberPagination
from .serializers import studentSerializers

@api_view(["GET"])
def list(request):
    try:
        student_list = student.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        serializer = studentSerializers(student_list, many= True)
        result = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response({"data":result, "message":"student list"})
    except student.DoesNotExist:
        return Response({"message":"data does not exist"})

@api_view(["POST"])
def create(request):
    try:
        objUser = request.data
        serializer = studentSerializers(data=objUser)
        print(objUser)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"student created"})

        return Response({"data":[],"error":serializer.errors, "message":"something is wrong"})
    except Exception as e:
        return Response({"message":e})

@api_view(["PUT"])
def update(request):
    try:
        objUser = request.data
        user_id = request.query_params.get('user_id')
        list = student.objects.get(pk = user_id)
        result = studentSerializers(list, data=request.data)
        if result.is_valid():
            result.save()
            return Response({"data":result.data, "message":"updated"})

        return Response({"data":"failed", "message":"student list"})
    except student.DoesNotExist:
        return Response({"message":"data does not exist"})


@api_view(["DELETE"])
def delete(request):
    try:
        user_id = request.query_params.get('user_id')
        list = student.objects.get(pk = user_id)
        result = studentSerializers(list)
        list.delete()

        return Response({"data":result.data, "message":"deleted"})
    except student.DoesNotExist:
        return Response({"message":"data does not exist"})


