"""assistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from assistant import view
from assistant.sitemaps import StaticViewSitemap, ApartmentSitemap, ResidenceSitemap, CommerceSitemap, LandSitemap, \
    ServiceSitemap

sitemaps = {
    'apartment': ApartmentSitemap,
    'residence': ResidenceSitemap,
    'commerce': CommerceSitemap,
    'land': LandSitemap,
    'static': StaticViewSitemap,
    'service': ServiceSitemap
}

urlpatterns = [
                  url(r'^$', view.index, name='index'),
                  url(r'^page/', include('assistant.additionalpage.urls')),
                  url(r'^service/', include('assistant.service.urls')),
                  url(r'^estate/', include('assistant.estate.urls')),
                  url(r'^partners/', include('assistant.marketing.urls')),
                  url(r'^contact/', view.contact, name='contact'),
                  url(r'^calculator/(?P<cost>[\w\-]+)', view.calculator),
                  url(r'^configuration/', view.configuration),
                  url(r'^get_apartment_geo/$', view.get_apartment_geo),
                  url(r'^get_apartments/$', view.get_apartments),
                  url(r'^get_cities/$', view.get_cities),
                  url(r'^get_districts/$', view.get_districts),
                  url(r'^get_streets/$', view.get_streets),
                  url(r'^get_constructions/$', view.get_constructions),
                  url(r'^get_residences/$', view.get_residences),
                  url(r'^get_residence_geo/$', view.get_residence_geo),
                  url(r'^get_residence_constructions/$', view.get_residence_constructions),
                  url(r'^get_commerces/$', view.get_commerces),
                  url(r'^get_commerce_geo/$', view.get_commerce_geo),
                  url(r'^get_commerce_constructions/$', view.get_commerce_constructions),
                  url(r'^get_appointments/$', view.get_appointments),
                  url(r'^get_land_geo/$', view.get_land_geo),
                  url(r'^get_lands/$', view.get_lands),
                  url(r'^get_land_appointment/$', view.get_land_appointment),
                  url(r'^send_mail/', view.send_email),
                  url(r'^send_wait_call/', view.send_wait_call),
                  url(r'^admin/', admin.site.urls),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
              ] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
