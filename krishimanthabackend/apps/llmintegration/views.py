from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.conf import settings
from .serializers import SummarizeRequestSerializer, QueryRequestSerializer, LLMResponseSerializer
from .services import LLMService


class SummarizeView(APIView):
    """POST /api/v1/llm/summarize/ — admin-only. Body: {"text": "..."}
    Scaffold endpoint for future AI features (e.g. auto-summarizing a long
    news article while drafting it in the admin panel)."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SummarizeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = LLMService().summarize(serializer.validated_data["text"])
        return Response(LLMResponseSerializer({"result": result, "provider": settings.LLM_PROVIDER}).data)


class QueryView(APIView):
    """POST /api/v1/llm/query/ — admin-only. Body: {"question": "...", "context": "..." }"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = QueryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        result = LLMService().answer_query(data["question"], data.get("context", ""))
        return Response(LLMResponseSerializer({"result": result, "provider": settings.LLM_PROVIDER}).data)
