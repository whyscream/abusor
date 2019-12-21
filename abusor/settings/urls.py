from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from rest_framework import routers

from abusor.events.views import CaseViewSet, EventViewSet

api = routers.DefaultRouter()
api.register(r'case', CaseViewSet)
api.register(r'event', EventViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(api.urls)),
    url(r'^$', TemplateView.as_view(template_name='frontend/index.html'))
]
