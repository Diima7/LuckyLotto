from django.contrib import admin
from django.urls import path, include

urlpatterns = [     #Haupt Project
    path('admin/', admin.site.urls),
    path('', include('webs.urls')),    #Die urls der webs App werden in dieses Url pattern importiert.
]
