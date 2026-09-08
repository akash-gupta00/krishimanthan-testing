from rest_framework import serializers
from .models import MarketPrice


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = ["id", "crop_name_hi", "crop_name_en", "price", "unit_hi", "unit_en", "trend"]
