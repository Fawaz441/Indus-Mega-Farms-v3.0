from django.contrib import admin
from .models import Post,Paragraph

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 30
    # max_num = 30

class PostAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline,]

admin.site.register(Post,PostAdmin)
admin.site.register(Paragraph)