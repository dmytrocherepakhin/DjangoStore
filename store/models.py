from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кількість")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Зображення")

    def __str__(self):
        return self.name
