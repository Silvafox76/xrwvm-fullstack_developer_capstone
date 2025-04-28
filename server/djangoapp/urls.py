# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for registration
    path('register/', views.registration, name='registration'),

    # path for login API
    path('login', views.login_user, name='login'),

    # path for login REACT page rendering
    path('login/', TemplateView.as_view(template_name="index.html")),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
