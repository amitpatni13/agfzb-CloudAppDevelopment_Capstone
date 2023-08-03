from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.
admin.site.register(CarModel)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'dealer_id', 'type', 'year')

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
