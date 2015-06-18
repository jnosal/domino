from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()


from apps.colors import api


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^api/v1/imagefile$',
        api.PostImagesApiController.as_view(),
        name='post-imagefile'
    ),
    url(
        r'^api/v1/imagefile/search$',
        api.ImageFileSearchController.as_view(),
        name='list-imagefile'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
