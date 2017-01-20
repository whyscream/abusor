from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from events.views import CaseViewSet, EventViewSet


router = routers.DefaultRouter()
router.register(r'api/case', CaseViewSet)
router.register(r'api/event', EventViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
]
