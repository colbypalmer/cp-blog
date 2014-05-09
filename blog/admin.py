from django.contrib import admin
from blog.models import BlogEntry, BlogCategory

class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'active', 'comments_open', 'view_count', 'edited_date')
    list_filter = ['status', 'active', 'comments_open']
    date_hierarchy = 'edited_date'
    search_fields = ['title', 'description', 'body']
    actions = ['delete_selected', 'make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Make selected entries active"

    def make_inactive(self, request, queryset):
        queryset.update(active=True)
    make_inactive.short_description = "Make selected entries inactive"
    
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'active','position')
    list_filter = ['active']
    search_fields = ['title']
    actions = ['delete_selected', 'make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Make selected categories active"

    def make_inactive(self, request, queryset):
        queryset.update(active=True)
    make_inactive.short_description = "Make selected categories inactive"
    

admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
