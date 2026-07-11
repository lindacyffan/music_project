from django.urls import path
from . import views
app_name = 'musicapp'

urlpatterns = [
    path('song/<int:song_id>/',views.song_detail,name='song_detail'),
    path('song/<int:song_id>/comment/',views.add_comment,name='add_comment'),
    path('song/<int:song_id>/comment/delete/<int:comment_id>/',views.delete_comment,name='delete_comment'),
    path('artists/',views.artist_list,name='artist_list'),
    path('artists/<int:artist_id>/',views.artist_detail,name='artist_detail'),
    path('playlists/',views.playlist_list,name = 'playlist_list'),
    path('playlists/<str:source>/', views.playlist_detail, name='playlist_detail'),
    path('search/',views.search,name = "search"),
    path('',views.song_list, name='song_list')
]