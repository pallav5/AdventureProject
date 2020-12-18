from django.db import models

# Create your models here.

from django.contrib.auth.models import User, Group
from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone

class Timetamp(models.Model):
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_active =models.BooleanField(default=True)

    def get_month(self):
        return self.updated_at.strftime('%b')

    def get_date(self):
        return self.updated_at.strftime('%d')

    def get_year(self):
        return self.updated_at.strftime('%y')

    def get_week(self):
        return self.updated_at.strftime('%a')

    def get_time(self):
        return self.updated_at.strftime('%I'":"'%M%p')

    class Meta:
        abstract = True


class Admin(Timetamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='admins', null= True, blank=True)
    phone = models.CharField(max_length=15,null=True , blank=True)
    role = models.CharField(max_length=100, choices=(
        ('Admin','Admin'),
        ('Staff', 'Staff'),
    ) , null=True, blank=True)
    about =models.TextField(null=True, blank=True)

    def save(self,*args,**kwargs):
        group, group_created = Group.objects.get_or_create(name='Admin')
        self.user.groups.add(group)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class Facilities(Timetamp):
    image = models.ImageField(upload_to='facilities/',null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title


class Features(Timetamp):
    image = models.ImageField(upload_to='features/',null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title



class Organization(Timetamp):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='organization')
    profile_image = models.ImageField(upload_to='organization')
    # profile_image2 = models.ImageField(upload_to='organization')


    profile_video = models.CharField(max_length=200, null=True, blank=True)
    profile_video_thumbnail = models.CharField(max_length=200, null=True, blank=True)
    vat_pan = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500)
    facilities = models.ManyToManyField(Facilities)
    features = models.ManyToManyField(Features)
    contact_no = models.CharField(max_length=200)
    alt_contact_no = models.CharField(max_length=200, null=True, blank=True)
    map_location = models.CharField(max_length=2000)
    email = models.EmailField()
    alt_email = models.EmailField(null=True, blank=True)
    about_us = models.TextField()
    mission_vision = models.TextField()

    facebook = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=200, null=True, blank=True)
    viber = models.CharField(max_length=200, null=True, blank=True)
    terms_and_conditions = models.TextField(null=True, blank=True)
    privacy_policy = models.TextField(null=True, blank=True)



    def __str__(self):
        return self.name



class RoomType(Timetamp):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='room/',null=True,blank=True)


    def __str__(self):
        return self.title


# Amenities = (
#     ('wifi','Wifi'),
#     ('tv','TV'),
#     ('ac','AC'),
#     ('phone','Phone'),
# )



class RoomServices(Timetamp):
    title = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title


# from adventureproject.tasks import set_room_as_available
class Room(Timetamp):
    title = models.CharField(max_length=200,null=True,blank=True)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    number = models.IntegerField(null=True,blank=True)
    services = models.ManyToManyField(RoomServices)
    features = models.ManyToManyField(Features,blank=True)
    is_reserved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='room/')
    image1 = models.ImageField(upload_to='room/', null=True, blank=True)
    image2 = models.ImageField(upload_to='room/', null=True, blank=True)
    image3 = models.ImageField(upload_to='room/', null=True, blank=True)
    image4 = models.ImageField(upload_to='room/', null=True, blank=True)
    image5 = models.ImageField(upload_to='room/', null=True, blank=True)
    max_person = models.IntegerField()
    size = models.IntegerField()
    no_of_beds = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f'{self.number}. {self.type} with {self.no_of_beds} beds for {self.max_person} people. id is {self.id} '






class Review(Timetamp):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    # roomreview = models.ForeignKey(Room,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=200,null=True,blank=True)
    quote = models.TextField(max_length=200)
    image = models.ImageField(upload_to="reviewers",null=True,blank=True)
    # profession = models.CharField(max_length=200,null=True,blank=True)



    def __str__(self):
        return self.name




class Booking(Timetamp):
    c_status = (('new','new'),
                       ('checked_out','checked_out'),
                       ('confirmed','confirmed'),
                       ('cancelled','cancelled'),
                       )
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField()
    email = models.EmailField()
    # confirm = models.BooleanField(default=False)
    customer_status = models.CharField(max_length=20,choices=c_status,default='new')
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=500,default='')
    description = models.TextField(null=True, blank=True)
    now = timezone.now().date()

    def __str__(self):
        return f'{self.first_name} {self.last_name} has booked room no.{self.room} from {self.check_in} upto {self.check_out} booking id is {self.id}'

    # def save(self, *args, **kwargs):
    #     super(Booking, self).save(*args, **kwargs)
    #     b = Booking.objects.get(id=self.id)
    #     a = Room.objects.get(id=b.room.id)
    #     # print(b)
    #     # super(Booking, self).save(*args, **kwargs)
    #     if ((b.check_out.date() >= self.now >= b.check_in.date())):
    #         a.is_reserved = True
    #
    #     # elif not b.check_out.date() >= self.now >= b.check_in.date() :
    #     #     a.is_reserved = False
    #     else:
    #         a.is_reserved = False
    #     a.save()

        # super(Booking, self).save(*args, **kwargs)





class Events(Timetamp):
    image = models.ImageField(upload_to='activities/')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

class EventImages(Timetamp):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='eventimages')
    image = models.ImageField(upload_to="event_gallery")

    def __str__(self):
        return self.event.title



    def get_month(self):
        return self.date.strftime('%b')

    def get_date(self):
        return self.date.strftime('%d')

    def get_year(self):
        return self.date.strftime('%y')


class Activities(Timetamp):
    image = models.ImageField(upload_to='activities/')
    title = models.CharField(max_length=200)
    description = models.TextField()


    def __str__(self):
        return self.title





class Slider(Timetamp):
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to="sliders")

    def __str__(self):
        return self.title





class ImageAlbum(Timetamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="gallery",null=False,blank=False)
    description = models.TextField(null=True, blank=True)

    def get_photos(self):
        return ImageMedia.objects.filter(album=self)

    # def thumbnail(self):
    #     return ImageMedia.image.filter(album=self.first())

    def __str__(self):
        return self.title


class ImageMedia(Timetamp):
    album = models.ForeignKey(ImageAlbum, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to="gallery")

    def __str__(self):
        return self.album.title



class Message(Timetamp):
    sender = models.CharField(max_length=200)
    mobile = models.CharField(max_length=40)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.sender


class Subscriber(Timetamp):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

