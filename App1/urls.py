from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='members'),
    path('create_stuff/', views.create_stuff, name='create_stuff'),
    path('stuff_list/', views.stuff_list, name='stuff_list'),
#    path('encrypt_all_data/', views.encryptData, name='encrypt_all_data'),
    path('delete_stuff/<int:stuff_id>/', views.delete_stuff, name='delete_stuff'),
    path('delete_stuff1/<int:stuff_id>/', views.delete_stuff1, name='delete_stuff1'),
    path('edit_stuff/<int:stuff_id>/', views.edit_stuff, name='edit_stuff'),
    path('success/', views.success, name='success'),
#    path('display/', views.display_decrypted_data, name='display_decrypted_data'),
    path('encrypt/', views.encrypt_file, name='encrypt'),
    path('decrypt/', views.decrypt_file, name='decrypt'),
]