from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from config.settings import MEDIA_URL, MEDIA_ROOT

from url.views import UrlList, UrlDetail, Home, Detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('Detail/<int:pk>', Detail.as_view(), name='detail'),
    path('url/', UrlList.as_view(), name='url-list-api'),
    path('url/<int:url_id>', UrlDetail.as_view(), name='url-detail-api')
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
