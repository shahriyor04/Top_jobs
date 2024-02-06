from django.urls import path, include

urlpatterns = [
    path('apps/', include('apps.urls')),

    path('blog/', include('blog.urls')),
    path('Token/', include('singin.urls')),
    path('chat/', include('chat_app.urls')),
    # path('google/', include('google_login.urls')),

    path('book/', include('book.url')),
    path('direct_video/', include('direct_video.urls')),

]
