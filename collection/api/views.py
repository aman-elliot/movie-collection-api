from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from .serializer import UserSerializer,CollectionSerializer,GenreSerializer,MovieSerializer,CollectionMovieSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from django.http import HttpResponse
import environ 
import requests
from base64 import b64encode
from django.http import JsonResponse
import json
from requests.adapters import HTTPAdapter,Retry
from rest_framework.permissions import IsAuthenticated
from collection.models import Collection,Movies,Genre,GenreStats,User,RequestCount
# Create your views here.


#default timeout 
DEFAULT_TIMEOUT = 5 # seconds

#setting timeout for requests
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


#combining timeout with retries for flaky third party api
http = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500])
http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
http.mount("http://", TimeoutHTTPAdapter(max_retries=retries))

#initialize environment
env = environ.Env()
environ.Env.read_env()

#user registration
@api_view(['POST'])
def userRegistration(request):
    
    #serializerclass
    serializer=UserSerializer(data=request.data)

    #deserialize
    if request.method == 'POST':
        if serializer.is_valid():
            serializer.save()
            #serialize
            return Response(serializer.data['token'], status=status.HTTP_201_CREATED)
        #if invalid serializer   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#base64 formatting
def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}' 


#list movies
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def listMovies(request):

    #basic auth
    if request.method == 'GET':
        username=env('UsernameForAPI')
        password=env('PasswordForAPI')
        headers = { 'Authorization' : basic_auth(username, password) }
        page=request.GET.get('page')
        print("page",type(page))

        if page=="1":
            response=http.get('https://demo.credy.in/api/v1/maya/movies/',headers=headers,timeout=1)
        else:
            response=http.get('https://demo.credy.in/api/v1/maya/movies/?page={}'.format(page),headers=headers,timeout=1)
        
        print(response.status_code)
        return JsonResponse(response.json())


#collection view
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated]) 
def listCollections(request):

    userObject=request.user
    
    # if the request is of type GET
    if request.method=='GET':
        
        querySet=userObject.collections.all()
        print("queryset",querySet)
        serializer=CollectionSerializer(querySet,many=True)

        res={
            "is_success": True,
            "data":{
                "collections":serializer.data
                },
            "favourite_genres":','.join([i.genre_name for i in GenreStats.objects.filter(user=userObject)[:3]])
        }
        return Response(res, status=status.HTTP_200_OK)

    # if the request is of type POST
    if request.method=='POST':
        print("username",request.user)
        request.data['user']=request.user.id
        serializer=CollectionSerializer(data=request.data)
        if serializer.is_valid():
            collectionInstance=serializer.save()
            print("collection instance",collectionInstance)
            collectionInstance.user=userObject
            print("serializerdata",serializer.data)
            d={'collection_uuid':serializer.data['uuid']}

            #update stats
            for movie in collectionInstance.movies.all():
                for genre in movie.genres.all():
                    obj,created = GenreStats.objects.get_or_create(user=userObject,genre_name=genre.genre_name)
                    if created == False:
                        obj.genre_count += 1
                    else:
                        obj.genre_count = 1


            return Response(d, status=status.HTTP_201_CREATED)
        #if invalid serializer   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#Operations on the movie list in the collection
@api_view(['GET','PUT','DELETE','PATCH'])
@permission_classes([IsAuthenticated]) 
def manipulate(request,collection_uuid):

    userObject=request.user

    #if the request is of type GET
    if request.method=='GET':
        print("collection uuid",collection_uuid)
        try:
            collectionObject=userObject.collections.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            return Response({"message":"Collection uuid not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer=CollectionMovieSerializer(collectionObject)
        return Response(serializer.data, status=status.HTTP_200_OK)


    #if the request is of type DELETE
    elif request.method=='DELETE':
        userObject.collections.get(uuid=collection_uuid).delete()
        return Response({"message":"collection with uuid " + collection_uuid+" deleted successfully"}, status=status.HTTP_200_OK)



    #if the request is of type PUT
    elif request.method=="PUT":
        request.data['user']=request.user.id
        
        try:
            collectionObject=userObject.collections.get(uuid=collection_uuid)
        except Collection.DoesNotExist:
            return Response({"message":"Collection uuid not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer=CollectionMovieSerializer(collectionObject,data=request.data,partial=True)
        if serializer.is_valid():
            collectionInstance=serializer.save()
            if "movies" in request.data:
                #update stats
                for movie in collectionInstance.movies.all():
                    for genre in movie.genres.all():
                        obj,created = GenreStats.objects.get_or_create(user=userObject,genre_name=genre.genre_name)
                        if created == False:
                            obj.genre_count += 1
                        else:
                            obj.genre_count = 1
            return Response({"message":"updated successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#update request count
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def updateRequestCount(request):
    if request.method=='GET':
        countObj=RequestCount.objects.all().first()
        request_count=countObj.requestCount
        print("request count",request_count)
        return Response({"requests":request_count},status=status.HTTP_200_OK)
    
#reset request count
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def resetRequestCount(request):
    if request.method=='POST':
        RequestCount.objects.all().delete()
        return Response({"message":"request count reset successfully"},status=status.HTTP_200_OK)