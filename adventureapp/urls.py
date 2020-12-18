from django.urls import path

from .views import *
from django.conf.urls import handler404


app_name = "adventureapp"

urlpatterns =[

#admin site
path('admin-site/login/', AdminLoginView.as_view(), name = 'adminlogin'),
path('', AdminHomeView.as_view(), name = 'adminhomeview'),
path('logout/', AdminLogoutView.as_view(), name = 'adminlogout'),
path('admin-home/', AdminHomeView.as_view(), name = 'adminhome'),
path('admin-create/', AdminCreateView.as_view(), name = 'admincreate'),
path('admin-profile/<int:pk>/', AdminProfileView.as_view(), name = 'adminprofile'),
path('admin-update/<int:pk>/', AdminProfileUpdateView.as_view(), name = 'adminprofileupdate'),
path('admin/change-password/', AdminPasswordUpdateView.as_view(), name = 'adminpasswordupdate'),
path('admin/base/', AdminBaseView.as_view(), name = 'adminbase'),

#Room type and rooms
path('admin/room-type/add/', AdminRoomTypeCreateView.as_view(), name = 'adminroomtypeadd'),
path('admin/room-type/update/<int:pk>/', AdminRoomTypeUpdateView.as_view(), name = 'adminroomtypeupdate'),
path('admin/room-type/delete/<int:pk>/', AdminRoomTypeDeleteView.as_view(), name = 'adminroomtypedelete'),


path('admin/room/detail/<int:pk>/', AdminRoomDetailView.as_view(), name = 'adminroomdetail'),
path('admin/room/list/', AdminRoomsListView.as_view(), name = 'adminroomlist'),
path('admin/room/add/', AdminRoomAddView.as_view(), name = 'adminroomadd'),
path('admin/room/update/<int:pk>/', AdminRoomUpdateView.as_view(), name = 'adminroomupdate'),
path('admin/room/delete/<int:pk>/', AdminRoomDeleteView.as_view(), name = 'adminroomdelete'),

path('admin/booking/list/', AdminBookingListView.as_view(), name = 'adminbookinglist'),
path('admin/booking/delete/<int:pk>/', AdminBookingDeleteView.as_view(), name = 'adminbookingdelete'),
path('admin/booking-history/list/', AdminBookingHistoryView.as_view(), name = 'adminbookinghistory'),
path('admin/booking-confirmed/list/', AdminBookingConfirmedListView.as_view(), name = 'adminbookingconfirmedlist'),
path('admin/booking/reserve/toggle/<int:pk>/', AdminBookingToggle.as_view(), name = 'adminbookingtoogle'),
path('admin/booking/confirm/toggle/<int:pk>/', AdminBookingConfirmToogle.as_view(), name = 'adminbookingconfirm'),
path('admin/booking/checkout/toggle/<int:pk>/', AdminBookingCheckoutToggle.as_view(), name = 'adminbookingcheckout'),

path('admin/booking-chart/', BookingChartView.as_view(), name = 'bookingchart'),
path('chart/<int:pk>/', C_statusView.as_view(), name = 'cstatusview'),

path('admin/room-availability/', RoomAvailability.as_view(), name = 'roomavailability'),


path('admin/organization/create/', AdminOrganizationFormView.as_view(), name = 'adminorganization'),
path('admin/organization/update/<int:pk>/', AdminOrganizationUpdateView.as_view(), name = 'adminorganizationupdate'),
# path('admin/organization/info/', OrganizationDetailView.as_view(), name = 'adminorganizationinfo'),


path('admin/subscribers/', AdminSubscribersListView.as_view(), name = 'adminsubscriberlist'),


path('admin/features/', AdminFeaturesView.as_view(), name = 'adminfeatures'),
path('admin/features/add/', AdminFeaturesAddView.as_view(), name = 'adminfeaturesadd'),
path('admin/features/update/<int:pk>/', AdminFeaturesUpdateView.as_view(), name = 'adminfeaturesupdate'),
path('admin/features/delete/<int:pk>/', AdminFeaturesDeleteView.as_view(), name = 'adminfeaturesdelete'),


path('admin/roomservices/', AdminRoomServicesView.as_view(), name = 'adminroomservices'),
path('admin/roomservices/add/', AdminRoomServicesAddView.as_view(), name = 'adminroomservicessadd'),
path('admin/roomservices/update/<int:pk>/', AdminRoomServicesUpdateView.as_view(), name = 'adminroomservicesupdate'),
path('admin/roomservices/delete/<int:pk>/', AdminRoomServicesDeleteView.as_view(), name = 'adminroomservicesdelete'),


path('admin/review/', AdminReviewView.as_view(), name = 'adminreviewlist'),
path('admin/review/delete/<int:pk>/', AdminReviewDeleteView.as_view(), name = 'adminreviewdelete'),



path('admin/imagealbum/create/', ImageAlbumAddView.as_view(), name = 'adminimagealbumadd'),
path('admin/imagealbum/list/', ImageAlbumListView.as_view(), name = 'adminimagealbumlist'),
path('admin/imagealbum/<int:pk>/detail/', ImageAlbumDetailView.as_view(), name = 'adminimagealbumdetail'),
path('admin/imagealbum/<int:pk>/update/', ImageAlbumUpdateView.as_view(), name = 'adminimagealbumupdate'),
path('admin/imagealbum/<int:pk>/delete/', ImageAlbumDeleteView.as_view(), name = 'adminimagealbumdelete'),


path('admin/imagemedia/<int:pk>/delete/', ImageMediaDeleteView.as_view(), name = 'adminimagemediadelete'),
# path('admin/imagemedia/<int:pk>/detail/', ImageMediaDetailView.as_view(), name = 'adminimagemediadetail'),


path('admin/activities/list/', AdminActivitiesListView.as_view(), name = 'adminactivitylist'),
path('admin/activities/add/', AdminActivitiesAddView.as_view(), name = 'adminactivityadd'),
path('admin/activities/update/<int:pk>/', AdminActivitiesUpdateView.as_view(), name = 'adminactivityupdate'),
path('admin/activities/delete/<int:pk>/', AdminActivitiesDeleteView.as_view(), name = 'adminactivitydelete'),



path('admin/facilities/list/', AdminFacilitiesListView.as_view(), name = 'adminfacilitieslist'),
path('admin/facilities/add/', AdminFacilitiesAddView.as_view(), name = 'adminfacilitiesadd'),
path('admin/facilities/update/<int:pk>/', AdminFacilitiesUpdateView.as_view(), name = 'adminfacilitiesupdate'),
path('admin/facilities/delete/<int:pk>/', AdminFacilitiesDeleteView.as_view(), name = 'adminfacilitiesdelete'),


path('admin/messages/list/', AdminMessageListView.as_view(), name = 'adminmessagelist'),
path('admin/messages/delete/<int:pk>/', AdminMessageDeleteView.as_view(), name = 'adminmessagedelete'),



path('admin/events/list/', AdminEventsListView.as_view(), name = 'admineventslist'),
path('admin/events/<int:pk>/detail/', AdminEventsDetailView.as_view(), name = 'admineventsdetail'),
path('admin/events/add/', AdminEventsAddView.as_view(), name = 'admineventsadd'),
path('admin/events/update/<int:pk>/', AdminEventsUpdateView.as_view(), name = 'admineventsupdate'),
path('admin/events/delete/<int:pk>/', AdminEventsDeleteView.as_view(), name = 'admineventsdelete'),

path('admin/event-images/delete/<int:pk>/', AdminEventsImageDeleteView.as_view(), name = 'admineventsimagedelete'),



# client views

path('client/room/list/', ClientRoomListView.as_view(), name = 'clientroomlist'),
path('client/booking/list/', ClientBookingListView.as_view(), name = 'clientbookinglist'),
path('client/room/booking/', ClientRoomBookingView.as_view(), name = 'clientroombooking'),
path('home/', ClientHome.as_view(), name = 'clienthome'),
path('client/clientmaxperson/', ClientMaxPersonRoomsView.as_view(), name = 'clientmaxperson'),
path('client/clientmaxperson-roomlist/', ClientMaxPersonRoomList.as_view(), name = 'clientmaxpersonroomlist'),
path('client/room-list/', ClientRoomListView.as_view(), name = 'clientroomlist'),
path('client/room-detail/<int:pk>/', ClientRoomDetailView.as_view(), name = 'clientroomdetail'),
path('client/contact/', ClientContactCreateView.as_view(), name = 'clientcontactcreate'),

# path('client/room/<int:pk>/review/', ClientRoomReviewFromDetailView.as_view(), name = 'clientroomreviewfromdetail'),


path('client/about-us/', ClientAboutUsView.as_view(), name = 'clientaboutus'),

path('client/subscribe/', SubscribeCreateView.as_view(), name = 'subscribercreate'),
path('client/subscriber/<int:pk>/delete/', ClientSubscriberDeleteView.as_view(), name = 'subscriberdelete'),

path('client/room/<int:pk>/book/', ClientRoomBookFromDetailView.as_view(), name = 'clientroombookfromdetail'),
path('client/gallery/', ClientGalleryView.as_view(), name = 'clientgallery'),
path('client/events/', ClientEventListView.as_view(), name = 'clienteventslist'),
path('client/events/<int:pk>/detail/', ClientEventDetailView.as_view(), name = 'clienteventsdetail'),
path('client/activities/', ClientActivityListView.as_view(), name = 'clientactivitylist'),
path('client/activities/<int:pk>/detail/', ClientActivityDetailView.as_view(), name = 'clientactivitydetail'),


path('client/reviews/create/', ClientReviewCreateView.as_view(), name = 'clientreviewcreate'),
# path('client/activities/<int:pk>/detail/', ClientActivityDetailView.as_view(), name = 'clientactivitydetail'),

]

handler404 = error_404_view