from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','name','user']

    class Meta:
        model = Admin

admin.site.register(
    Admin,UserAdmin

)


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','title']

    class Meta:
        model = RoomType

admin.site.register(
    RoomType,RoomAdmin

)

admin.site.register(Booking)

admin.site.register([Room])
admin.site.register(Organization)
admin.site.register(Facilities)
admin.site.register(Activities)
admin.site.register(Slider)
admin.site.register(Review)
# admin.site.register(ImageAlbum)


class ImagemediaInline(admin.TabularInline):
    model = ImageMedia
    extra = 5

class ImageAlbumAdmin(admin.ModelAdmin):
    inlines = [ ImagemediaInline, ]

admin.site.register(ImageAlbum,ImageAlbumAdmin)

class EventsInline(admin.TabularInline):
    model = EventImages
    extra = 5

class EventsImagesAdmin(admin.ModelAdmin):
    inlines = [ EventsInline, ]

admin.site.register(Events,EventsImagesAdmin)
admin.site.register(RoomServices)
admin.site.register(Message)
admin.site.register(Subscriber)
admin.site.register(Features)




