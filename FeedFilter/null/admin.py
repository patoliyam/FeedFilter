from null.models import *
from django.contrib import  admin

admin.site.register(BlockedPost)
admin.site.register(Tag)

class  PostAdmin(admin.ModelAdmin):
    list_display = ("post_id" , "sentiments")

admin.site.register(Post,PostAdmin)
