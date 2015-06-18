from django.contrib import admin

from .models import Color, ImageFile


class ColorInline(admin.TabularInline):
    extra = 1
    model = Color
    fields = ('name', 'hex', 'r', 'g', 'b')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex', 'r', 'g', 'b', 'image',)


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    list_display = ('basename', 'created_at', 'updated_at',)
    inlines = [ColorInline]