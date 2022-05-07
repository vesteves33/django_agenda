from encodings import search_function
from django.contrib import admin
from .models import Category, Contact

class ContactAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'telephone', 'email', 'description', 'category', 'show')
  list_display_links = ('id', 'name')
  list_filter = ('name','category')
  list_per_page = 10
  search_fields = ('name', 'telephone', 'category')
  list_editable = ('telephone','show',)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name',)
  list_filter = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact, ContactAdmin)