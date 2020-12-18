from django import forms

from django_summernote.widgets import SummernoteWidget
from .models import *
from simplemathcaptcha.fields import MathCaptchaField
from simplemathcaptcha.widgets import MathCaptchaWidget



class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter username...',
               'class': 'input100', 'id': 'loginuname'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter password...',
               'class': 'input100', 'id': 'loginpword'}))



class AdminProfileForm(forms.ModelForm):

    class Meta:
        model = Admin
        fields = ['name', 'email','phone', 'image', 'role', 'about',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control select-single'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }

class PasswordUpdateForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter current password',
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter new password',
    }))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm new password',
    }))

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New passwords did not match!")


class AdminRoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = "__all__"

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title',

            }),


            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Desc..',
                'rows': 5,

        }),
    }

class AdminRoomAddForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = "__all__"

        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title',

            }),
            'type': forms.Select(attrs={
                'class': 'form-control singleselect'
            }),
            'services': forms.SelectMultiple(attrs={
                'class': 'form-control multipleselect'
            }),
            'features': forms.SelectMultiple(attrs={
                'class': 'form-control multipleselect'
            }),


            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),'image4': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),'image5': forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),
            'description': SummernoteWidget(),
    }


class ClientRoomBookingForm(forms.ModelForm):
    captcha = MathCaptchaField(widget=MathCaptchaWidget(
        question_tmpl="What is the result of %(num1)i %(operator)s %(num2)i?",

        attrs={'class': 'form-control input-sm',

               'placeholder': 'Please Answer this question!'
               },

    ))
    error_messages = {'invalid': ('Please check your math and try again.'),
                      'invalid_number': ('Enter a whole number.')}
    class Meta:
        model = Booking
        fields = "__all__"
        exclude = [ 'customer_status', ]
        widgets = {
            'room' : forms.Select(attrs={
            'class': 'form-control select-single text-dark',
                'style': 'border: 1px solid red;'
        }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control  text-dark',


            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control text-dark ',

            }),
            'check_in': forms.DateInput(attrs={
                'class': 'form-control text-dark',
                'type': 'date'

            }),
            'check_out': forms.DateInput(attrs={
                'class': 'form-control text-dark',
                'type': 'date'

            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control text-dark ',

            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control text-dark ',

            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control text-dark',

            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control col-md-12 text-dark ',
                'placeholder': 'Desc..',

                "style": "height: 170px;"
            }),

        }


class ChartForm(forms.ModelForm):
    # customer_status = forms.CharField()
    class Meta:
        model = Booking
        fields = ('customer_status',)
        widgets = {'customer_status': forms.Select(attrs={
                'class': 'form-control singleselect'
            }),}



class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"
        exclude = ('vat_pan',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family:BalaramFont',
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'profile_video': forms.URLInput(attrs={
                'class': 'form-control',
            }),
            'vat_pan': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'facilities': forms.SelectMultiple(attrs={
                'class': 'form-control multipleselect'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'contact_no': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'alt_contact_no': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'map_location': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'pattern': '[\w\.-]+@[\w\.-]+\.\w{2,4}'
            }),
            'alt_email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'about_us':forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'mission_vision': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'facebook': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'instagram': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'twitter': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'youtube': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'viber': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'terms_and_conditions': SummernoteWidget(),
            'privacy_policy': SummernoteWidget(),



        }

class ClientMaxPersonRooms(forms.Form):
    max_person = forms.FloatField(required=True,widget=forms.NumberInput(attrs={
                 'class': 'form-control ',
                 'placeholder':'no.s of people'

            }))
    check_in = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control ',
        'type': 'date'

    }))
    check_out = forms.DateTimeField(required=True, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'

    }))
    # room = forms.ModelChoiceField(queryset=Room.objects.all(), required=True, widget=forms.Select(attrs={
    #     'class': 'form-control select-single'
    # }))


class ClientMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            'sender': forms.TextInput(attrs={
                'class': 'form-control  text-dark',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control  text-dark',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control  text-dark',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control  text-dark',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control  text-dark',
                'rows': 5,

            }),

        }

class RoomDetailBookingForm(forms.ModelForm):
    captcha = MathCaptchaField(widget=MathCaptchaWidget(
        question_tmpl="What is the result of %(num1)i %(operator)s %(num2)i?",

        attrs={'class': 'form-control input-sm',

               'placeholder': 'Please Answer this question!'
               },

    ))
    error_messages = {'invalid': ('Please check your math and try again.'),
                      'invalid_number': ('Enter a whole number.')}
    class Meta:
        model = Booking
        fields = "__all__"
        exclude = ['room','customer_status',]
        widgets = {

            'first_name' :forms.TextInput(attrs={
            'class': 'form-control ',

        }),
        'last_name' : forms.TextInput(attrs={
            'class': 'form-control ',

        }),
        'check_in' : forms.DateInput(attrs={
            'class': 'form-control ',
            'type': 'date'

        }),
        'check_out' : forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'

        }),
        'email' : forms.EmailInput(attrs={
            'class': 'form-control ',

        }),
        'address' : forms.TextInput(attrs={
            'class': 'form-control ',

        }),
        'phone' : forms.NumberInput(attrs={
            'class': 'form-control ',

        }),
        'description' : forms.Textarea(attrs={
            'class': 'form-control col-md-12 ',
            'placeholder': 'Desc..',

            "style": "height: 170px;"
        }),

        }
        from six import text_type
from django.http import JsonResponse
class SubscribeForm(forms.ModelForm):
    captcha = MathCaptchaField(widget=MathCaptchaWidget(
           question_tmpl="What is the result of %(num1)i %(operator)s %(num2)i?",

        attrs={'class': 'form-control input-sm',

                'placeholder': 'Please Answer this question!'
               },

                ))
    error_messages = {'invalid': ('Please check your math and try again.'),
                      'invalid_number': ('Enter a whole number.')}

    class Meta:
        model = Subscriber
        fields = "__all__"

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control input-lg text-white ',
                'type': 'email',

                'placeholder': 'Your Email'
            }),

        }

        error_messages = {'captcha': {'invalid': ('Please check your math and try again.'),
                          'invalid_number': ('Enter a whole number.')}}



class FeaturesForm(forms.ModelForm):
    class Meta:
        model = Features
        fields = "__all__"
        exclude = ['is_active']

        widgets = {
            'description' : forms.Textarea(attrs={
            'class': 'form-control col-md-12 ',
            'placeholder': 'Desc..',

            "style": "height: 170px;"
        }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family:BalaramFont',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }



class RoomServicesForm(forms.ModelForm):
    class Meta:
        model = RoomServices
        fields = "__all__"
        exclude = ['is_active']

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family:BalaramFont',
            }),
            'icon': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class OrgFacilitiesForm(forms.ModelForm):
    class Meta:
        model = Facilities
        fields = "__all__"
        exclude = ['is_active']

        widgets = {
            'description' : forms.Textarea(attrs={
            'class': 'form-control col-md-12 ',
            'placeholder': 'Desc..',

            "style": "height: 170px;"
        }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family:BalaramFont',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = "__all__"
        exclude = ['is_active']

        widgets = {
            'description' : forms.Textarea(attrs={
            'class': 'form-control col-md-12 ',
            'placeholder': 'Desc..',

            "style": "height: 170px;"
        }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family:BalaramFont',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class FacilitiesForm(forms.ModelForm):
    class Meta:
        model = Facilities
        fields = "__all__"
        exclude = ['is_active']

        widgets = {
            'description' : forms.Textarea(attrs={
            'class': 'form-control col-md-12 ',
            'placeholder': 'Desc..',

            "style": "height: 170px;"
        }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'font-family:BalaramFont',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


class ReviewForm(forms.ModelForm):
    # captcha = MathCaptchaField(widget=MathCaptchaWidget(
    #     question_tmpl="What is the result of %(num1)i %(operator)s %(num2)i?",
    #
    #     attrs={'class': 'form-control input-sm font-weight-bold text-dark',
    #            'style': 'border: 1px solid black; ',
    #
    #            'placeholder': 'Please Answer this question!'
    #            },
    #
    # ))
    # error_messages = {'invalid': ('Please check your math and try again.'),
    #                   'invalid_number': ('Enter a whole number.')}
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ['is_active']

        widgets = {
            'quote' : forms.Textarea(attrs={
            'class': 'form-control col-md-12 font-weight-bold text-dark ',
            'placeholder': 'What would you like to say!!',

            "style": "height: 170px;""border: 1px solid black;",
        }),
            'name': forms.TextInput(attrs={
                'class': 'form-control font-weight-bold text-dark',
                'style': "border: 1px solid black;",
                'placeholder': 'Your full name',
            }),
            'topic': forms.TextInput(attrs={
                'class': 'form-control font-weight-bold text-dark',
                'style': "border: 1px solid black;",
                'placeholder': 'Review topic',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control font-weight-bold text-dark',
                'style': "border: 1px solid black;",
                'placeholder': 'Your address',
            }), 'email': forms.EmailInput(attrs={
                'class': 'form-control font-weight-bold text-dark',
                'style': "border: 1px solid black;",
                'placeholder': 'Your email',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control font-weight-bold text-dark',
                'style':"border: 1px solid black;",

            }),
        }



# class RoomReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = "__all__"
#         exclude = ['is_active','roomreview']
#
#         widgets = {
#             'quote' : forms.Textarea( attrs={
#             'class': 'form-control col-md-12  text-dark ',
#             'placeholder': 'Max-200 letters',
#
#             "style": "height: 170px;"
#         }),
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control  text-dark',
#
#             }),'profession': forms.TextInput(attrs={
#                 'class': 'form-control  text-dark',
#
#             }),
#             'address': forms.TextInput(attrs={
#                 'class': 'form-control  text-dark',
#                 'style': 'font-family:BalaramFont',
#             }),
#             'image': forms.ClearableFileInput(attrs={
#                 'class': 'form-control  text-dark',
#             }),
#         }


class ImageAlbumForm(forms.ModelForm):
    class Meta:
        model = ImageAlbum
        fields = "__all__"
        # exclude = ()
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control col-md-12 ',
                'placeholder': 'Desc..',

                "style": "height: 170px;"
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                # 'style': 'font-family:BalaramFont',
            }),


        }




#
# class ImageMediaForm(forms.ModelForm):
#     class Meta:
#         model = ImageMedia
#         fields = "__all__"
#         widgets = {
#
#             'album': forms.Select(attrs={
#                 'class': 'form-control singleselect'
#             }), }


from django.forms.models import inlineformset_factory,formset_factory
ImageMediaFormSet = inlineformset_factory(
    ImageAlbum,ImageMedia, fields=['image'],can_delete = True,
    widgets= {
        'image': forms.ClearableFileInput(attrs={
            'class': 'form-control',
        }),

    }
)


EventsFormSet = inlineformset_factory(
    Events,EventImages, fields=['image'],can_delete = True,
    widgets= {
        'image': forms.ClearableFileInput(attrs={
            'class': 'form-control',
        }),

    }
)


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = "__all__"
        exclude = ('is_active',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control col-md-12 ',
                'placeholder': 'Desc..',

                "style": "height: 170px;"
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'date': forms.DateInput(attrs={
                'class':'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
            }),



        }

