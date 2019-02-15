from django.db import models
from django.core.validators import MinValueValidator


class TodoItem(models.Model):
    title = models.CharField(max_length=256)
    completed = models.BooleanField(blank=True, default=False)
    order = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )

    @classmethod
    def get_next_order_num(cls):
        last_item = cls.objects.values('order').order_by('order').last()
        if not last_item or last_item['order'] is None:
            return 1
        return last_item['order'] + 1
