from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.views.generic import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
import datetime
from .check_availability import check_availability
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mass_mail,send_mail
import json
from django.core import mail
from django.http import JsonResponse


def error_404_view(request,exception):
    print('lauaaaaaaaaaaaaaaaaaaaaa')
    return render(request, '404.html', status=404)




class AdminLoginView(FormView):
    template_name = "authtemplates/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy("adventureapp:adminhome")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,password = password)
        if user is not None and user.groups.filter(name = 'Admin').exists():
            login(self.request,user)
        else:
            return render(self.request, self.template_name,{
                'form' : form,
                'error' : 'invalid credentials'
            })
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return self.success_url



class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('adventureapp:adminlogin')

# from django.http import HttpResponseRedirect
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="Admin").exists():
            pass
        else:
            return redirect('/admin-site/login/?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['org'] = Organization.objects.first()


        return context

class AdminCreateView(CreateView):
    template_name = "admintemplates/adminhome.html"
    form_class = AdminProfileForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email= form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username=name,email= email, password = password)
        user.save()
        # print('superuser created')
        return redirect('/')



class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name = "admintemplates/admindashboard.html"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        context['bookings'] = Booking.objects.filter(customer_status='new')
        context['subscriber'] = Subscriber.objects.all()
        context['features'] = Features.objects.all()
        context['roomservice'] = RoomServices.objects.all()
        context['review'] = Review.objects.all()
        context['album'] = ImageAlbum.objects.all()
        context['activities'] = Activities.objects.all()
        context['facilities'] = Facilities.objects.all()
        context['messages'] = Message.objects.all()
        context['events'] = Events.objects.all()

        return context




class AdminProfileUpdateView(AdminRequiredMixin,UpdateView):
    model = Admin
    template_name = 'admintemplates/adminprofileupdate.html'
    form_class = AdminProfileForm
    success_message = "Profile was updated"
    def get_success_url(self):
        return reverse('adventureapp:adminprofile',
                       kwargs={'pk':self.kwargs['pk']})



class AdminProfileView(AdminRequiredMixin,TemplateView):
    template_name = "admintemplates/adminprofile.html"

    def get_context_data(self, **kwargs):

        # print(self.request.user)
        context = super().get_context_data(**kwargs)
        context["admin"] = Admin.objects.get(user = self.request.user)
        return context



class AdminPasswordUpdateView( FormView):
    template_name = 'admintemplates/adminpasswordupdate.html'
    form_class = PasswordUpdateForm
    success_url = reverse_lazy("adventureapp:adminhome")
    success_message = "Password updated successfully. \
                        Please Login to continue."

    def form_valid(self, form):
        current_password = form.cleaned_data['current_password']
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = authenticate(username=self.request.user.username,
                            password=current_password)
        if user is not None:
            user.set_password(confirm_new_password)
            user.save()
        else:
            return render(self.request, self.template_name, {
                'form': form,

                'admin': Admin.objects.get(user=self.request.user),
                'error': "Invalid Current Password!"})
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('adventureapp:adminupdate',
    #                    kwargs={'pk': self.request.user.admin.id})


class AdminBaseView(AdminRequiredMixin,TemplateView):
    template_name = 'admintemplates/adminbase.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = Booking.objects.all()


        return context




class AdminRoomTypeCreateView(AdminRequiredMixin,CreateView):
    template_name ='admintemplates/adminroomtypecreate.html'
    form_class = AdminRoomTypeForm
    success_url = '/admin/room/list/'

class AdminRoomTypeUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admintemplates/adminroomtypecreate.html'
    form_class = AdminRoomTypeForm
    model = RoomType
    success_url = '/admin/room/list/'

class AdminRoomTypeDeleteView(AdminRequiredMixin, DeleteView):
    template_name = 'admintemplates/adminroomtypedelete.html'


    model = RoomType
    success_url = reverse_lazy('adventureapp:adminroomlist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AdminRoomDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admintemplates/adminroomdetail.html'
    model = Room
    # form_class = AdminRoomAddForm
    context_object_name = 'roomdetail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = AdminRoomAddForm()
    #     return context


class AdminRoomsListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminroomtypelist.html'
    queryset = Room.objects.all()

    context_object_name = 'roomlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roomtypelist'] = RoomType.objects.all()
        context['roomservice'] = RoomType.objects.all()
        context['roomfeatures'] = Features.objects.all()
        return context

class AdminRoomAddView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminroomadd.html'
    form_class = AdminRoomAddForm
    model = Room
    success_url = reverse_lazy('adventureapp:adminroomlist')

    # def form_valid(self, form):
    #     self.type = form.save()
    #     return super().form_valid(form)



class AdminRoomUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/adminroomadd.html'
    form_class = AdminRoomAddForm
    model = Room
    success_url = '/admin/room/list/'



class AdminRoomDeleteView(AdminRequiredMixin,DeleteView):
    template_name = 'admintemplates/adminroomdelete.html'
    model = Room
    success_url = reverse_lazy('adventureapp:adminroomlist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AdminBookingListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminbookinglist.html'
    model = Booking
    context_object_name = 'bookings'


class AdminBookingDeleteView(AdminRequiredMixin,DeleteView):
    template_name = 'admintemplates/adminbookinglist.html'
    model = Booking
    success_url = reverse_lazy('adventureapp:adminbookinglist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)





class AdminBookingHistoryView(AdminRequiredMixin,ListView):
    model = Booking
    template_name = 'admintemplates/adminbookinghistory.html'
    context_object_name = 'bookinghistory'


class AdminBookingConfirmedListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminbookingconfirmedlist.html'
    model = Booking
    context_object_name = 'bookingconfirmed'



class AdminBookingToggle(AdminRequiredMixin,View):

    def get(self, request,*args,**kwargs):
        # print(self.kwargs)
        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        # print(room.id)
        booking = Booking.objects.filter(room_id=room.id)
        # print(booking)
        now = timezone.now()
        for books in booking:
            if books.check_in <= now < books.check_out:
                return HttpResponse('room is currently occupied')
            else:
                books.room.is_reserved = not room.is_reserved
                books.room.save()

        return redirect('adventureapp:adminroomlist')


class AdminBookingConfirmToogle(AdminRequiredMixin,View):
    now = timezone.now()
    def get(self, request,*args,**kwargs):
        # print(self.kwargs)
        booking = get_object_or_404(Booking, pk=self.kwargs['pk'])
        # print(booking.room.is_reserved)
        if booking.check_out >= self.now >= booking.check_in:
            booking.room.is_reserved = True
        else:
            booking.room.is_reserved = False
        booking.room.save()
        booking.customer_status = "confirmed"
        booking.save()
        return redirect('adventureapp:adminbookinglist')


class RoomAvailability(AdminRequiredMixin,View):
    def get(self, *args, **kwargs):
        # a = Room.objects
        book = Booking.objects.all()
        now = timezone.now()
        # print(book)

        for b in book:
            # print(b.check_out)
            if b.check_out <= now:
                b.room.is_reserved = False
                b.customer_status = 'checked_out'
                b.save()
            # elif b.customer_status == 'cancelled':
            #     b.delete()


            # elif b.check_out >= now >= b.check_in and b.customer_status == 'confirmed':
            #     b.room.is_reserved = True
            #
            # b.room.save()

        return redirect('adventureapp:adminhome')


class AdminBookingCheckoutToggle(AdminRequiredMixin,View):
    def get(self, request,*args,**kwargs):
        # print(self.kwargs)
        booking = get_object_or_404(Booking,pk=self.kwargs['pk'])

        booking.room.is_reserved = False
        booking.room.save()
        booking.customer_status = 'checked_out'
        booking.save()
        return redirect('adventureapp:adminbookingconfirmedlist')



class AdminOrganizationFormView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminorganization.html'
    # print(Organization.objects.all())
    model = Organization
    form_class = OrganizationForm

    success_url = reverse_lazy("adventureapp:adminorganization")



class AdminOrganizationUpdateView(AdminRequiredMixin,UpdateView):
    template_name = 'admintemplates/adminorganization.html'

    model = Organization
    form_class = OrganizationForm

    success_url = reverse_lazy("adventureapp:adminhome")




class BookingChartView(TemplateView):
    template_name = 'admintemplates/bookingchart.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = Booking.objects.all()
        context['room'] = Room.objects.all()
        context['roomtype'] = RoomType.objects.all()
        context['c_status'] = list(Booking.c_status)
        context['c_form'] = ChartForm
        return context



class C_statusView(View):

    def get(self, request, *args, **kwargs):

        form = ChartForm()
        return render(request, 'admintemplates/bookingchart.html', {'forms': form})

    def post(self, request,*args,**kwargs):
        a = kwargs['pk']
        # print(a)
        global customer_status

        # print('ulalalalalalal')
        # print(request.POST)
        form = ChartForm(request.POST)
        booking = Booking.objects.all()
        # a = booking.id

        if form.is_valid():
            now = timezone.now()

            form.save(commit=False)
            obj = Booking.objects.get(id=a)
            # print(obj)

            customer_status = form.cleaned_data['customer_status']



            if ((obj.check_out >= now >= obj.check_in) and customer_status == 'confirmed'):
                obj.room.is_reserved = True
            elif (obj.check_out >= now >= obj.check_in):
                obj.room.is_reserved = False

            obj.room.save()


            obj.customer_status = customer_status
            obj.save()
            if obj.customer_status == 'cancelled':
                obj.delete()
            return HttpResponse('success')


        context = {'forms': form, 'customer_status': customer_status,'booking':booking}
        return render(request, 'admintemplates/bookingchart.html', context)



class AdminSubscribersListView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminsubscribers.html'
    model = Subscriber
    context_object_name = 'subscribers'

class AdminFeaturesView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminfeatures.html'
    model = Features
    context_object_name = 'features'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['features'] = Features.objects.all()
    #     return context


class AdminFeaturesAddView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminfeaturesadd.html'
    model = Features
    form_class = FeaturesForm
    context_object_name = 'features'
    success_url = reverse_lazy('adventureapp:adminfeatures')


class AdminFeaturesUpdateView(UpdateView):
    template_name = 'admintemplates/adminfeaturesadd.html'
    model = Features
    form_class = FeaturesForm
    success_url = reverse_lazy('adventureapp:adminfeatures')


class AdminFeaturesDeleteView(AdminRequiredMixin,DeleteView):
    template_name = 'admintemplates/adminfeaturedelete.html'
    model = Features
    success_url = reverse_lazy('adventureapp:adminfeatures')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AdminRoomServicesView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminroomservices.html'
    model = RoomServices
    context_object_name = 'roomservices'



class AdminRoomServicesAddView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminroomservicesadd.html'
    form_class = RoomServicesForm
    context_object_name = 'features'
    success_url = reverse_lazy('adventureapp:adminroomservices')


class AdminRoomServicesUpdateView(UpdateView):
    template_name = 'admintemplates/adminroomservicesadd.html'
    form_class = RoomServicesForm
    success_url = reverse_lazy('adventureapp:adminroomservices')


class AdminRoomServicesDeleteView(AdminRequiredMixin,DeleteView):

    model = RoomServices
    success_url = reverse_lazy('adventureapp:adminroomservices')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AdminReviewView(AdminRequiredMixin,ListView):
    template_name = 'admintemplates/adminreviewlist.html'
    model = Review
    context_object_name = 'review'

class AdminReviewDeleteView(AdminRequiredMixin,DeleteView):

    model = Review
    success_url = reverse_lazy('adventureapp:adminreviewlist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AdminActivitiesListView(AdminRequiredMixin,ListView):
    model = Activities
    template_name = 'admintemplates/adminactivitylist.html'
    context_object_name = 'activities'



class AdminActivitiesAddView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminactivityadd.html'
    form_class = ActivitiesForm

    success_url = reverse_lazy('adventureapp:adminactivitylist')


class AdminActivitiesUpdateView(UpdateView):
    model = Activities
    template_name = 'admintemplates/adminactivityadd.html'
    form_class = ActivitiesForm
    success_url = reverse_lazy('adventureapp:adminactivitylist')


class AdminActivitiesDeleteView(AdminRequiredMixin,DeleteView):

    model = Activities
    success_url = reverse_lazy('adventureapp:adminactivitylist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)





class AdminFacilitiesListView(AdminRequiredMixin,ListView):
    model = Facilities
    template_name = 'admintemplates/adminfacilitieslist.html'
    context_object_name = 'facilities'



class AdminFacilitiesAddView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/adminfacilitiesadd.html'
    form_class = FacilitiesForm

    success_url = reverse_lazy('adventureapp:admifacilitieslist')


class AdminFacilitiesUpdateView(UpdateView):

    template_name = 'admintemplates/adminfacilitiesadd.html'
    form_class = FacilitiesForm
    success_url = reverse_lazy('adventureapp:admifacilitieslist')


class AdminFacilitiesDeleteView(AdminRequiredMixin,DeleteView):

    model = Facilities
    success_url = reverse_lazy('adventureapp:admifacilitieslist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)





class AdminMessageListView(AdminRequiredMixin,ListView):
    model = Message
    template_name = 'admintemplates/adminmessagelist.html'
    context_object_name = 'messages'





class AdminMessageDeleteView(AdminRequiredMixin,DeleteView):

    model = Message
    success_url = reverse_lazy('adventureapp:adminmessagelist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)







class AdminEventsListView(AdminRequiredMixin,ListView):
    model = Events
    template_name = 'admintemplates/admineventslist.html'
    context_object_name = 'events'


class AdminEventsDetailView(AdminRequiredMixin,DetailView):
    model = Events
    template_name = 'admintemplates/admineventsdetail.html'
    success_url = reverse_lazy('adventureapp:admineventslist')

    context_object_name = 'eventdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = EventImages.objects.filter(event__id=self.kwargs.get('pk'))
        return context

class AdminEventsImageDeleteView(AdminRequiredMixin, DeleteView):
    model = EventImages
    template_name = 'admintemplates/admineventslist.html'
    success_url = reverse_lazy('adventureapp:admineventslist')




class AdminEventsAddView(AdminRequiredMixin,CreateView):
    template_name = 'admintemplates/admineventsadd.html'
    form_class = EventsForm

    success_url = reverse_lazy('adventureapp:admineventslist')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        event_formset= EventsFormSet()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  event_formset = event_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        event_formset = EventsFormSet(self.request.POST , self.request.FILES )
        # print(imagemedia_form.cleaned_data)

        if (form.is_valid() and event_formset.is_valid()):
            return self.form_valid(form, event_formset)
        else:
            return self.form_invalid(form, event_formset)

    def form_valid(self, form, event_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        # print('=======')
        # print(self.object)
        self.object = form.save()
        event_formset.instance = self.object
        # print('=======')
        # print(self.object)
        event_formset.save()


        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, event_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  event_formset=event_formset))






class AdminEventsUpdateView(AdminRequiredMixin,UpdateView):
    model = Events
    template_name = 'admintemplates/admineventsadd.html'
    form_class = EventsForm
    success_url = reverse_lazy('adventureapp:admineventslist')


    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        event = Events.objects.get(pk=kwargs.get('pk'))
        # print(album)

        event_formset = EventsFormSet(instance = event)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  event_formset= event_formset,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        event = Events.objects.get(pk=kwargs.get('pk'))
        event_formset = EventsFormSet(self.request.POST , self.request.FILES, instance = event )
        # print(event_formset.cleaned_data)

        if (form.is_valid() and event_formset.is_valid()):
            return self.form_valid(form, event_formset)
        else:
            return self.form_invalid(form, event_formset)

    def form_valid(self, form, event_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        # print('=======')
        # print(self.object)
        self.object = form.save()
        event_formset.instance = self.object
        # print('=======')
        # print(self.object)
        event_formset.save()


        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, event_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  event_formset=event_formset))




class AdminEventsDeleteView(AdminRequiredMixin,DeleteView):

    model = Events
    success_url = reverse_lazy('adventureapp:admineventslist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)












from django.http import HttpResponse, HttpResponseRedirect
class ImageAlbumAddView(AdminRequiredMixin, CreateView):
    model = ImageMedia
    form_class = ImageAlbumForm
    template_name = 'admintemplates/imagealbumadd.html'
    success_url = reverse_lazy('adventureapp:adminhome')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imagemedia_form = ImageMediaFormSet()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  imagemedia_form = imagemedia_form,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imagemedia_form = ImageMediaFormSet(self.request.POST , self.request.FILES )
        # print(imagemedia_form.cleaned_data)

        if (form.is_valid() and imagemedia_form.is_valid()):
            return self.form_valid(form, imagemedia_form)
        else:
            return self.form_invalid(form, imagemedia_form)

    def form_valid(self, form, imagemedia_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        # print('=======')
        # print(self.object)
        self.object = form.save()
        imagemedia_form.instance = self.object
        # print('=======')
        # print(self.object)
        imagemedia_form.save()


        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, imagemedia_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  imagemedia_form=imagemedia_form))



class ImageAlbumUpdateView(AdminRequiredMixin, UpdateView):
    model = ImageAlbum
    form_class = ImageAlbumForm
    formset_class = ImageMediaFormSet
    is_update_view = True
    template_name = 'admintemplates/imagealbumadd.html'
    success_url = reverse_lazy('adventureapp:adminhome')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        album = ImageAlbum.objects.get(pk=kwargs.get('pk'))
        # print(album)

        imagemedia_form = ImageMediaFormSet(instance = album)

        return self.render_to_response(
            self.get_context_data(form=form,
                                  imagemedia_form=imagemedia_form,
                                  ))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        album = ImageAlbum.objects.get(pk=kwargs.get('pk'))
        imagemedia_form = ImageMediaFormSet(self.request.POST , self.request.FILES, instance = album )
        print(imagemedia_form.cleaned_data)

        if (form.is_valid() and imagemedia_form.is_valid()):
            return self.form_valid(form, imagemedia_form)
        else:
            return self.form_invalid(form, imagemedia_form)

    def form_valid(self, form, imagemedia_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        # print('=======')
        # print(self.object)
        self.object = form.save()
        imagemedia_form.instance = self.object
        # print('=======')
        # print(self.object)
        imagemedia_form.save()


        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, imagemedia_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  imagemedia_form=imagemedia_form))


class ImageMediaDeleteView(AdminRequiredMixin, DeleteView):
    model = ImageMedia
    template_name = 'admintemplates/imagemediadelete.html'
    success_url = reverse_lazy('adventureapp:adminhome')

#
# class ImageMediaDetailView(AdminRequiredMixin, DetailView):
#     model = ImageMedia
#     template_name = 'admintemplates/adminimagemediadetail.html'
#     success_url = reverse_lazy('adventureapp:adminhome')




class ImageAlbumListView(AdminRequiredMixin, ListView):
    model = ImageAlbum
    context_object_name = 'albums'

    template_name = 'admintemplates/adminimagealbumlist.html'




class ImageAlbumDetailView(AdminRequiredMixin, DetailView):
    model = ImageAlbum
    template_name = 'admintemplates/adminimagealbumdetail.html'
    success_url = reverse_lazy('adventureapp:adminimagealbumlist')

    context_object_name = 'albumdetail'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['imagemedias'] = ImageMedia.objects.filter(album__id=self.kwargs.get('pk'))


        return context


class ImageAlbumDeleteView(AdminRequiredMixin, DeleteView):
    model = ImageAlbum
    # template_name = 'admintemplates/adminimagealbumdelete.html'
    success_url = reverse_lazy('adventureapp:adminimagealbumlist')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)






# client views start


class ClientRequiredMixin(object):

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['org'] = Organization.objects.first()
        context['hotelpic'] = Room.objects.first()
        context['hotelpic1'] = Room.objects.last()
        context['galleryimage'] = ImageMedia.objects.all()
        context['subscribeform'] = SubscribeForm
        context['rooms'] = Room.objects.all()


        return context


class ClientBaseView(ClientRequiredMixin,TemplateView):
    template_name = 'clienttemplates/clientbase.html'




class ClientBookingListView(ListView):
    model = Booking
    template_name = 'clienttemplates/clientbookinglist.html'
    context_object_name = 'booking'



class ClientRoomBookingView(ClientRequiredMixin,FormView):

    form_class = ClientRoomBookingForm
    template_name = 'clienttemplates/clientroombooking.html'


    def form_valid(self, form):
        data = form.cleaned_data
        # print(data)
        # print('===========================')
        room = data['room']
        room_list = Room.objects.filter(type=room.type)

        booking = Booking.objects.filter(room=room)
        # print(data['check_out'])
        # print('---')
        available_rooms = []
        for room in room_list:

            if check_availability(room,data['check_in'],data['check_out']):
                available_rooms.append(room)
        # for books in booking:
        #     if books.customer_status =='cancelled':
        #         available_rooms.append(books.room)
        #         books.delete()
        #     books.save()



        # print(booking)
        # print('--------')
            # print(data['check_in'])

        if len(available_rooms)>0:

            for room in available_rooms:
                booking = Booking.objects.create(
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    email = data['email'],
                    address = data['address'],
                    room = room,
                    check_in= data['check_in'],
                    check_out= data['check_out'],
                    phone = data['phone'],
                    description= data['description'],


                )

                booking.save()
                return HttpResponse(booking)
        else:
            return HttpResponse('So sorry to inform you that this room is already booked! at that time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookingform'] = ClientRoomBookingForm
        return context




class ClientMaxPersonRoomsView(ClientRequiredMixin,FormView):

    form_class = ClientMaxPersonRooms
    template_name = 'clienttemplates/clienthome.html'

    def form_valid(self, form):
        data = form.cleaned_data
        maxperson = data['max_person']
        rooms = Room.objects.all()
        available_rooms = []
        array = []


        for room in rooms:

            if check_availability(room,data['check_in'],data['check_out']) and room.max_person >= maxperson:
                available_rooms.append(room)
                # print(available_rooms)

        for x in range(len(available_rooms)):
            avail_room = available_rooms[x]
            array.append(avail_room.id)

        a = Room.objects.filter(id__in=array)
        # print(a)
        if len(available_rooms)>0:
            context = {
                'maxpersonroom': available_rooms,
                'maxpersonroomlist': a,
                'org': Organization.objects.first(),
                'form': SubscribeForm
            }

            return render(self.request,'clienttemplates/clientmaxpersonroomlist.html',context)
        else:
            return HttpResponse('So sorry to inform you that this room is already booked! at that time')


class ClientHome(ClientRequiredMixin,TemplateView):
    template_name = 'clienttemplates/clienthome.html'
    # print(Review.objects.filter(roomreview__isnull=True ))


    a = Events.objects.all().order_by('-id')[:3]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientmaxpersonform'] = ClientMaxPersonRooms
        context['reviews'] = Review.objects.all()[:5]
        context['hotelpics'] = ImageMedia.objects.filter(album__title ='Hotel')
        context['carouselpics'] = ImageMedia.objects.all()
        context['rooms'] = Room.objects.all()
        context['latestevents'] = Events.objects.all().order_by('-id')[:3]
        context['activities'] = Activities.objects.all().order_by('-id')[:3]
        return context



class ClientMaxPersonRoomList(ClientRequiredMixin,TemplateView):
    template_name = 'clienttemplates/clientmaxpersonroomlist.html'


class ClientRoomListView(ClientRequiredMixin,ListView):
    model = Room
    context_object_name = 'clientroomlist'
    template_name = 'clienttemplates/clientroomlist.html'
    paginate_by = 4


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientmaxpersonform'] = ClientMaxPersonRooms
        return context


class ClientRoomDetailView(ClientRequiredMixin,DetailView):
    model = Room

    context_object_name = 'clientroomdetail'
    template_name = 'clienttemplates/clientroomdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookfromdetailform'] = RoomDetailBookingForm
        # context['roomreviewform'] = RoomReviewForm
        # context['roomreviews'] = Review.objects.filter(roomreview__id = self.kwargs.get('pk'))

        return context


class ClientRoomReviewFromDetailView(ClientRequiredMixin,CreateView):
    template_name = 'clienttemplates/clientroomdetail.html'
    # form_class = RoomReviewForm
    model = Booking
    success_message = "Thank you for your review"

    def get_success_url(self):
        return reverse_lazy('adventureapp:clientroomdetail',kwargs = {'pk':self.object.room_id})

    def form_valid(self, form):
        form.instance.roomreview = Room.objects.get(id=self.kwargs.get('pk'))
        room = Room.objects.get(id=self.kwargs.get('pk'))
        form.save()

        return HttpResponse(room)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # context['roomreviewform'] = RoomReviewForm

        return context


class ClientAboutUsView(ClientRequiredMixin,TemplateView):
    template_name = 'clienttemplates/clientaboutus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roompics'] = Room.objects.first()
        context['albums'] = ImageAlbum.objects.all()
        context['activities'] = Activities.objects.all().order_by('-id')[:3]

        return context


class ClientContactCreateView(ClientRequiredMixin, CreateView):

    template_name = "clienttemplates/clientcontact.html"
    form_class = ClientMessageForm
    success_url = reverse_lazy('adventureapp:clientcontactcreate')
    success_message = "Thank you for contacting us."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['contactform'] = ClientMessageForm
        return context

class ClientRoomBookFromDetailView(ClientRequiredMixin,CreateView):
    template_name = 'clienttemplates/clientroomdetail.html'
    form_class = RoomDetailBookingForm
    model = Booking

    def get_success_url(self):
        return reverse_lazy('adventureapp:clientroomdetail',kwargs = {'pk':self.object.room_id})

    def form_valid(self, form):
        form.instance.room = Room.objects.get(id=self.kwargs.get('pk'))
        data = form.cleaned_data
        room = Room.objects.get(id=self.kwargs.get('pk'))
        room_list = Room.objects.filter(type=room.type)
        available_rooms = []
        for room in room_list:

            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
        if len(available_rooms) > 0:
            for room in available_rooms:
                booking = Booking.objects.create(
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    email = data['email'],
                    address = data['address'],
                    room = room,
                    check_in= data['check_in'],
                    check_out= data['check_out'],
                    phone = data['phone'],
                    description= data['description'],


                )

                booking.save()
            return HttpResponse(room)
        else:
            return HttpResponse('So sorry to inform you that this room is already booked! at that time')

        return super().form_valid(form)




class SubscribeCreateView(ClientRequiredMixin, CreateView):
    template_name = "clienttemplates/clientbase.html"
    form_class = SubscribeForm
    success_url = reverse_lazy('adventureapp:clienthome')
    # success_message = "Thank you for subscribing us!!!"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if Subscriber.objects.filter(email=email).exists():
            print('==================')

            data = {
                'errorss': "Subscriber already exists."
            }


            return JsonResponse(data)
        else:
            form.save()
            # subject = 'Site contact form'
            # from_email = settings.EMAIL_HOST_USER
            # contact_message = "Thanks for subscribing us (Adventure Jungle Resort)."
            # send_mail(subject,
            #           contact_message,
            #           from_email,
            #           [email],
            #           fail_silently=False)

            data = {
                'success': "Thank you for subscribing us!"
            }

            return JsonResponse(data)


        return super().form_valid(form)

        # def form_invalid(self, form):
        #     email = form.cleaned_data["email"]
        #     data = {
        #         'errorss': "Subscriber already exists1111111111"
        #     }
        #     if Subscriber.objects.filter(email=email).exists():
        #
        #         return JsonResponse(data)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['forms'] = MyForm
    #
    #     return context


class ClientSubscriberDeleteView(ClientRequiredMixin,DeleteView):
    model = Subscriber
    success_url = reverse_lazy('adventureapp:adminsubscriberlist')


    def get(self,request,*args,**kwargs):
        return self.delete(request,*args,**kwargs)





class ClientGalleryView(ClientRequiredMixin,TemplateView):

    template_name = 'clienttemplates/clientgallery.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = ImageAlbum.objects.all()

        return context


class ClientEventListView(ClientRequiredMixin,ListView):

    template_name = 'clienttemplates/clienteventslist.html'
    model = Events
    queryset = Events.objects.all().order_by('-id')
    context_object_name = 'events'
    paginate_by = 3



class ClientEventDetailView(ClientRequiredMixin,DetailView):

    template_name = 'clienttemplates/clienteventsdetail.html'
    model = Events
    context_object_name = 'events'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['allevents'] = Events.objects.all().order_by('-id')[:3]
        context['subscribeform'] = SubscribeForm
        context['eventimages'] = EventImages.objects.filter(event__id=self.kwargs.get('pk'))

        # print('-----------------')
        # print(EventImages.objects.filter(event__id=self.kwargs.get('pk')))
        return context

class ClientActivityListView(ClientRequiredMixin,ListView):

    template_name = 'clienttemplates/clientactivitylist.html'
    model = Activities
    context_object_name = 'activities'
    # paginate_by = 3


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #
    #     return context



class ClientActivityDetailView(ClientRequiredMixin,DetailView):

    template_name = 'clienttemplates/clientactivitydetail.html'
    model = Activities
    context_object_name = 'activity'
    # paginate_by = 3


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #
    #     return context



class ClientReviewCreateView(ClientRequiredMixin,CreateView):

    template_name = 'clienttemplates/clientreviewscreate.html'
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('adventureapp:clientreviewcreate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all().order_by()
        context['reviewform'] = ReviewForm
        return context

    # paginate_by = 3


