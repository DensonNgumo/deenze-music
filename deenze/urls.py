
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from music import views as music_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$',music_views.index,name='index'),
     url(r'^view_songs/(?P<filter_by>[a-zA_Z]+)/$',music_views.songs,name='songs'),
    url(r'^create_album/$',music_views.create_album,name='create_album'),
    url(r'^favorite_album/(?P<album_id>[0-9]+)/$',music_views.favorite_album,name='fav_album'),
    url(r'^delete_album/(?P<album_id>[0-9]+)/$',music_views.delete_album,name='del_album'),
    url(r'^detail/(?P<album_id>[0-9]+)/$',music_views.detail,name='detail'),
    url(r'^detail/(?P<album_id>[0-9]+)/add_song/$',music_views.add_song,name='add_song'),
    url(r'^detail/(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$',music_views.delete_song,name='delete_song'),
    url(r'^detail/fav_song/(?P<song_id>[0-9]+)/$',music_views.favorite_song,name='fav_song'),



]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)