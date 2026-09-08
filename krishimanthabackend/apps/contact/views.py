from rest_framework import mixins, viewsets
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """POST /api/v1/contact/ — public contact form handler."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            send_mail(
                subject=f"[Krishi Manthan Contact] {instance.subject or 'New message'}",
                message=f"From: {instance.name} <{instance.email}>\n\n{instance.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
