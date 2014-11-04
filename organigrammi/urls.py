# # -*- coding: utf-8 -*-
# from __future__ import absolute_import
#
# from datetime import date
#
# from django.conf.urls import patterns, url
#
# from .views import (ConsiglioComunaleYearArchiveView,
#                     ConsiglioComunaleMonthArchiveView,
#                     ConsiglioComunaleDetailView,
#                     ConsiglioComunaleListView,
#                     EventiIstituzionaliHomeView)
#
#
# urlpatterns = patterns(
#     'opa_trasparenza.views',
#     url(r'^events/$', EventiIstituzionaliHomeView.as_view(),
#         name='events_list'),
#     url(r'^events/consigliocomunale/$',
#         ConsiglioComunaleListView.as_view(),
#         name='consiglicomunali_list'),
#     url(r'^events/consigliocomunale/(?P<year>\d{4})/$',
#         ConsiglioComunaleYearArchiveView.as_view(),
#         name='consiglicomunali_year_archive'),
#     url(r'^events/consigliocomunale/(?P<year>\d{4})/(?P<month>\d+)/$',
#         ConsiglioComunaleMonthArchiveView.as_view(month_format='%m'),
#         name='consiglicomunali_month_archive'),
#     url(r'^events/consigliocomunale/(?P<year>\d{4})/(?P<month>\d+)/(?P<pk>\d+)/$',
#         ConsiglioComunaleDetailView.as_view(),
#         name='consiglicomunali_detail'),
# )
