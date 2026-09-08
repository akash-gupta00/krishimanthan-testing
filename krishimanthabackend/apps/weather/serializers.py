from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    city_hi = serializers.CharField()
    city_en = serializers.CharField()
    temp_c = serializers.FloatField()
    condition_hi = serializers.CharField()
    condition_en = serializers.CharField()
    humidity = serializers.IntegerField()
    wind_kmh = serializers.FloatField()
    source = serializers.CharField()
