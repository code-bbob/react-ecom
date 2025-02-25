from rest_framework import serializers
from .models import Product, Comment, Repliess, ProductImage, Rating
from django.contrib.auth.models import User

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() #yo garexi i can define serializers for user by myself i.e. user ko kun attribute pathaune vanera
    comment = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Repliess
        fields = ['user', 'comment','text','published_date']
    def get_user(self, obj):
        return obj.user.name

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() #yo garexi i can define serializers for user by myself i.e. user ko kun attribute pathaune vanera
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.name
    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only = True)
    product = serializers.PrimaryKeyRelatedField(read_only =True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Rating
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.name
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    
class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many = True, read_only = True)
    # rating = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        # extra_fields = ['comments', 'images', 'rating']
    
    # def get_rating(self, obj):
    #     ratings = Rating.objects.filter(product=obj)
    #     if ratings.exists():
    #         total_ratings = ratings.count()
    #         #show how many stars ratings were rated acc to each star
    #         rating_dict = {1:0, 2:0, 3:0, 4:0, 5:0}
    #         for rating in ratings:
    #             rating_dict[rating.rating] += 1
    #         avg_rating = sum(rating.rating for rating in ratings) / len(ratings)
    #         avg_rating = round(avg_rating, 1)
    #         return {'total_ratings': total_ratings, 'rating_dict': rating_dict, 'avg_rating': avg_rating}
    #     return {'total_ratings': 0, 'rating_dict': {1:0, 2:0, 3:0, 4:0, 5:0}, 'avg_rating': 0}

    def get_ratings(self,obj):
        request = self.context.get('request')
        stats = {}
        ratings = Rating.objects.filter(product=obj)
        if ratings.exists():
            total_ratings = ratings.count()
            #show how many stars ratings were rated acc to each star
            rating_dict = {1:0, 2:0, 3:0, 4:0, 5:0}
            for rating in ratings:
                rating_dict[rating.rating] += 1
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings)
            avg_rating = round(avg_rating, 1)
            stats = {'total_ratings': total_ratings, 'rating_dict': rating_dict, 'avg_rating': avg_rating}
        else:
            stats = {'total_ratings': 0, 'rating_dict': {1:0, 2:0, 3:0, 4:0, 5:0}, 'avg_rating':0}
        serializer = RatingSerializer(ratings, many=True, context={'request': request})
        return {"stats":stats, "data":serializer.data}
