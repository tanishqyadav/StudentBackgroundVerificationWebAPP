# inside application doc verification

from django.urls import path
from . import views

urlpatterns = [
     
     path('documentvrecieved/', views.verification_doc_recieved),
     path('documentvrecieved/addrn/<int:vid>',views.addrn),
     path('documentvrecieved/addrn/alotthem/<int:vid>', views.allotment),

     path('list/', views.common_listing),
     path('list/searchcomlist', views.searchcomlist),

     path('verifythese', views.verifytheselist),
     path('verifythese/verifythis/<int:k>', views.search_for_verification),
     path('verifythese/verifythis/addtoverified/<int:k>', views.addtoverified),
     path('verifythese/verifythis/notverified/<int:k>', views.notverified),
     
     path('dispatch/<int:k>', views.send_dispatch),
     # # path('uploadmedia/',views.uploadmedia),
     path('dreport/', views.reportdatewise),
     path('rdreport/', views.reportgenrefdept),
     path('dashboard/',views.dashboard),
     
     path('revisit', views.revisit), #spcl feature for rellotment

     
]