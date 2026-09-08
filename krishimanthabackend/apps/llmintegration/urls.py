from django.urls import path
from .views import SummarizeView, QueryView

urlpatterns = [
    path("summarize/", SummarizeView.as_view(), name="llm_summarize"),
    path("query/", QueryView.as_view(), name="llm_query"),
]
