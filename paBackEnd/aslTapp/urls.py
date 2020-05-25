from django.conf.urls import url, include
import aslTapp.views


urlpatterns = [
        url(r'submitImage$', aslTapp.views.submitImage)
    ]