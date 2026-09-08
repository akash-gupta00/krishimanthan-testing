from django.db import models
from tinymce.models import HTMLField
from apps.core.models import TimeStampedModel, PublishableModel


class FAQ(TimeStampedModel, PublishableModel):
    question_hi = models.CharField(max_length=300)
    question_en = models.CharField(max_length=300)
    answer_hi = HTMLField()
    answer_en = HTMLField()
    category = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question_en
