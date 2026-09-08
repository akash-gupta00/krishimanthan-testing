from rest_framework import serializers


class SummarizeRequestSerializer(serializers.Serializer):
    text = serializers.CharField()


class QueryRequestSerializer(serializers.Serializer):
    question = serializers.CharField()
    context = serializers.CharField(required=False, allow_blank=True)


class LLMResponseSerializer(serializers.Serializer):
    result = serializers.CharField()
    provider = serializers.CharField()
