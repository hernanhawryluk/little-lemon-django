from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 30, db_index = True)
    slug = models.SlugField(max_length = 30, db_index = True, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Menu(models.Model):
    category = models.ForeignKey('Category', on_delete = models.PROTECT)
    name = models.CharField(max_length = 50, db_index = True)
    slug = models.SlugField(max_length = 50, db_index = True)
    description = models.TextField(max_length = 255)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits = 10, decimal_places = 2, db_index = True)
    stock = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.name} : {str(self.price)}'

    class Meta:
        ordering = ['name']
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'