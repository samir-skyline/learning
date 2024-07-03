from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.pagination import PageNumberPagination
from .models import Person
from .serializer import PersonSerializers, personDefaultFields

@api_view(["GET"])
def getList(request):
    # person = Person.objects.all()
    # result = PersonSerializers(person, many=True)        
    # return Response({"data":result.data, "message":"List"})

    paginator = PageNumberPagination()
    paginator.page_size = 100  # Override the default page size if necessary

   
    list = personDefaultFields.copy()
    list.pop()
    print(list)
    persons = Person.objects.all()
    result_page = paginator.paginate_queryset(persons, request)
    result = PersonSerializers(result_page, many=True)
    return paginator.get_paginated_response({"data": result.data, "message": "List"})


@api_view(["POST"])
def create(request):
    objUser = request.data
    result = PersonSerializers(data = objUser)
    if result.is_valid():
        result.save()
        return Response({"Message":"save succcesss"})
    return Response({"Error":result.errors})

@api_view(["PUT"])
def update(request):
    user_id = request.query_params.get('userId')
    try:
        data = Person.objects.get(pk = user_id)
    except Person.DoesNotExist:
        return Response({"Message":"user does not exist"})
    result = PersonSerializers(data, data= request.data)
    if result.is_valid():
        result.save()
        return Response({"Message":"update sucecess"})
    return Response({"Error":result.errors})

@api_view(["DELETE"])
def delete(request):
    try:
        id = request.query_params.get('userId')
        user = Person.objects.get(pk = id)
        user.delete()
        return Response({"Message":"Delete done"})
    except Person.DoesNotExist:
        return Response({"Message":"user does not exist"})
    
    


# Register
@api_view(['POST'])
def register(request):
    serializer = PersonSerializers(data=request.data)
    if serializer.is_valid():
        person_data = serializer.validated_data
        person = Person.objects.create(
            full_name=person_data['full_name'],
            email=person_data['email']
        )
        person.set_password(person_data['password'])  # Set and hash the password
        person.save()
        return Response({'message': 'Person registered successfully', 'id': person.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Login
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        person = Person.objects.get(email=email)
        serializer = PersonSerializers(person)
        userInfo = serializer.data
        print(userInfo, "-----")
        if userInfo.get('password') == password:
            del userInfo['password']
            refresh = RefreshToken.for_user(person)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'user': userInfo}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except Person.DoesNotExist:
        return Response({'error': 'Person with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)


def token_refresh(request):
    refresh_token = request.data.get('refresh_token')

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_access_token(request):
    access_token = request.headers.get('Authorization').split(' ')[1]  # Assuming 'Bearer <token>' format

    if access_token:
        try:
            AccessToken(access_token).check_valid()
            return Response({'message': 'Access token is valid'}, status=status.HTTP_200_OK)
        except InvalidToken:
            return Response({'error': 'Access token is expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Access token is required'}, status=status.HTTP_400_BAD_REQUEST)