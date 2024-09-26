from django.urls import path,include
from .views.auth_views import RegisterView, LoginView, LogoutView
from .views.event_views import AllEventsView, EventsDetailView, EventDelete, EventUpdateView
from .views.showinfo_views import ShowInfoDelete, ShowInfoUpdateView
from .views.template import OperationPageView, HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('operation/', OperationPageView.as_view(), name='operation'),
    path('operation/delete/event/<str:pk>/', EventDelete.as_view(), name='event_delete'),
    path('operation/delete/showinfo/<int:pk>/', ShowInfoDelete.as_view(), name='showinfo_delete'),
    path('operation/update/event/<str:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('operation/update/showinfo/<int:pk>/', ShowInfoUpdateView.as_view(), name='showinfo_update'),
    path('operation/events/', AllEventsView.as_view(), name='event_list'),
    path('operation/events/<str:pk>/', EventsDetailView.as_view(), name='event_detail'),
]

