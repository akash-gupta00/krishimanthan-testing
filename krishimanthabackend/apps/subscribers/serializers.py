from rest_framework import serializers
from .models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["id", "name", "email", "mobile"]

    def validate_email(self, value):
        if Subscriber.objects.filter(email__iexact=value, is_active=True).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value
