from rest_framework import serializers

from watchlist_app.models import WatchList,StreamPlatform,Reviews

class ReviewsSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Reviews
        exclude=('watchlist',)
        #fields='__all__'

class WatchListSerializer(serializers.ModelSerializer):
    reviews=ReviewsSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name',read_only=True)
    class Meta:
        model=WatchList
        fields='__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist= WatchListSerializer(many=True,read_only=True)

    class Meta:
        model=StreamPlatform
        fields='__all__'





# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too short")
#
# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(max_length=50,validators=[name_length])
#     description=serializers.CharField(max_length=200)
#     active=serializers.BooleanField(default=True)
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.active=validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#
#     def validate(self,data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Title and Description should be different")
#         else:
#             return data

    # def validate_name(self,value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too short")
    #     else:
    #         return value