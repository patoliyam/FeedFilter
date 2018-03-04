from null.models import *
from django.contrib import  admin

admin.site.register(BlockedPost)
admin.site.register(Tag)
admin.site.register(Stats)
admin.site.register(UserTag)
admin.site.register(UserPost)


# class  PostAdmin(admin.ModelAdmin):
#     list_display = ("post_id" , "sentiments")

# admin.site.register(Post,PostAdmin)
