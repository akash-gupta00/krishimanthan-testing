from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from apps.news.models import NewsItem
from apps.schemes.models import Scheme
from apps.events.models import Event
from apps.resources.models import Resource


class SearchView(APIView):
    """
    GET /api/v1/search/?q=kisan

    Unified search across News, Schemes, Events and Resources — mirrors the
    shape the frontend's SearchBar/searchIndex.ts already expects, so the
    only frontend change needed is pointing searchContent() at this URL.
    """

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if len(q) < 2:
            return Response([])

        results = []

        for item in NewsItem.objects.filter(is_published=True).filter(
            Q(title_hi__icontains=q) | Q(title_en__icontains=q) | Q(summary_hi__icontains=q) | Q(summary_en__icontains=q)
        )[:5]:
            results.append({
                "id": f"news-{item.id}", "type": "news",
                "title_hi": item.title_hi, "title_en": item.title_en,
                "subtitle_hi": item.category.name_hi if item.category else "",
                "subtitle_en": item.category.name_en if item.category else "",
                "url": "/news",
            })

        for item in Scheme.objects.filter(is_published=True).filter(
            Q(name_hi__icontains=q) | Q(name_en__icontains=q) | Q(overview_hi__icontains=q) | Q(overview_en__icontains=q)
        )[:5]:
            results.append({
                "id": f"scheme-{item.id}", "type": "scheme",
                "title_hi": item.name_hi, "title_en": item.name_en,
                "subtitle_hi": "सरकारी योजना", "subtitle_en": "Government Scheme",
                "url": "/schemes",
            })

        for item in Event.objects.filter(is_published=True).filter(
            Q(title_hi__icontains=q) | Q(title_en__icontains=q) | Q(location_hi__icontains=q) | Q(location_en__icontains=q)
        )[:5]:
            results.append({
                "id": f"event-{item.id}", "type": "event",
                "title_hi": item.title_hi, "title_en": item.title_en,
                "subtitle_hi": item.location_hi, "subtitle_en": item.location_en,
                "url": "/events",
            })

        for item in Resource.objects.filter(is_published=True).filter(
            Q(name_hi__icontains=q) | Q(name_en__icontains=q)
        )[:5]:
            results.append({
                "id": f"resource-{item.id}", "type": "resource",
                "title_hi": item.name_hi, "title_en": item.name_en,
                "subtitle_hi": "संसाधन", "subtitle_en": "Resource",
                "url": "/resources",
            })

        return Response(results[:8])
