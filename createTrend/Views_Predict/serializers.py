from rest_framework import serializers

class ViewsPredictSerializers(serializers.Serializer):
    thumbnail = serializers.ImageField()
    video_name = serializers.CharField()
    channel_subscriber = serializers.IntegerField()
    upload_date = serializers.DateField()