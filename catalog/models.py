from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price_cents = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_available"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name

# Create your models here.
