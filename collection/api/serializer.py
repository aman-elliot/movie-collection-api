
from rest_framework import serializers
from django.contrib.auth.models import User
from collection.models import Collection,Movies,Genre,GenreStats
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    #get_{field} 
    class Meta:
        model = User
        fields = ['username', 'password','token']
    
    
    def get_token(self,user):
        print(user)
        refresh = RefreshToken.for_user(user)

        return {
        # 'refresh': str(refresh),
        'access_token': str(refresh.access_token)
            }

    def validate_password(self, data):
        return make_password(data)


    # def validate_password(self,data):
    #     print("data",data)
    #     if len(data)<10:
    #         raise serializers.ValidationError("length of password must be greater than 10")
    #     return data

    # def validate_email(self,data):
    #     print("data",data)
    #     if len(data)<18:
    #         raise serializers.ValidationError("age should be more than 18")
    #     return data

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']



class MovieSerializer(serializers.ModelSerializer):
    genres=GenreSerializer(many=True)
    class Meta:
        model = Movies
        fields = ['title','description','genres','uuid']

    def create(self,validated):
        genres = validated.pop("genres")
        print("genre validated",genres)
        movie_obj = Movies.objects.create(**validated)
        for genre in genres:
            print("genre",genre)
            genre_serializer = GenreSerializer(data=genre)
            if genre_serializer.is_valid():
                genre_instance=genre_serializer.save()
                genre_instance.movie.add(movie_obj)
        return movie_obj

class CollectionSerializer(serializers.ModelSerializer):
    movies=MovieSerializer(many=True,write_only=True)
    class Meta:
        model = Collection
        fields = ['title','uuid','description','movies','user']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def create(self,validated):
        print("validated data", validated)
        movies = validated.pop("movies")
        collection_obj = Collection.objects.create(**validated)
        for movie_dict in movies:
            movie_serializer = MovieSerializer(data=movie_dict)
            # collection_obj.add(movie_instance)
            if movie_serializer.is_valid():
                movie_instance=movie_serializer.save()
                movie_instance.collection.add(collection_obj)

        return collection_obj
    # def create(self, validated_data):
    #     return super().create(validated_data)
    # def get_favourite_genres(self,collectionObject):
    #     return ','.join([i.genre_name for i in GenreStats.objects.filter(collection=collectionObject)])


class CollectionMovieSerializer(serializers.ModelSerializer):
    movies=MovieSerializer(many=True)
    class Meta:
        model = Collection
        fields = ['title','description','movies','user']
        extra_kwargs = {
            'user': {'write_only': True}
        }
    
    def update(self, instance, validated_data): 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        if "movies" in validated_data:
            movie_serializer = MovieSerializer(data = validated_data["movies"], many=True)
            if movie_serializer.is_valid():
                movie_qs=movie_serializer.save()
            for movie_instance in movie_qs:
                movie_instance.collection.add(instance)
        instance.save()
        return instance

