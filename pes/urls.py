from django.urls import path
from .views import RegisterView,filter_pes_events_by_fspid, LoginView, UserView, LogoutView,AddRandomCode,ChangePassword,CheckCodeExist,events_list,events_create,EventsRetrieveUpdateDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password/reset/', AddRandomCode.as_view()),
    path('password/check_code/', CheckCodeExist.as_view()),
    path('password/change_password/', ChangePassword.as_view()),
    path('events/',events_list, name='events-list'),
    path('create_events/',events_create, name='events-create'),
    path('events/<int:pk>/', EventsRetrieveUpdateDeleteView.as_view(), name='events-retrieve-update-delete'),
    path('filterFSPID/<int:fspid>/', filter_pes_events_by_fspid, name='get_fspid_record'),
    # path('create_record/', CreateRecordAPIView.as_view()),

]

