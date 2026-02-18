from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="نام محصول")
    price = models.CharField(max_length=100, verbose_name="قیمت")
    image_url = models.URLField(verbose_name="لینک تصویر")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name