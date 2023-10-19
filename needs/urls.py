from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # API routes
    path('add-need/', views.add_need, name='add_need'),
    path('add-action/', views.add_action, name='add_action'),
    path('delete-need/<int:need_id>/', views.delete_need, name='delete_need'),
    path('enact-action/<int:action_id>/',
         views.enact_action, name='enact_action'),
]
