from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=100, verbose_name='메뉴 이름')
    description = models.TextField(verbose_name='메뉴 설명')
    price = models.IntegerField(verbose_name='가격')
    total_servings = models.IntegerField(verbose_name='총 준비 수량')
    sold_servings = models.IntegerField(default=0, verbose_name='판매된 수량')
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True, verbose_name='메뉴 이미지')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def remaining_servings(self):
        return self.total_servings - self.sold_servings

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '메뉴'
        verbose_name_plural = '메뉴'
