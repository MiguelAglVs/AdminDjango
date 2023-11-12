from django.contrib import admin
from django.urls import path
from panel import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.signin, name='signin'),
    path('signin/', views.signin, name='signin'),
	path('signup/', views.signup, name='signup'),
	path('home/', views.index, name='home'),
    path('logout/', views.signout, name='logout'),
    path('users/', views.users, name='users'),
    path('persons/', views.persons, name='persons'),
    path('update_person/<int:persona_dni>/', views.update_person, name='update_person'),
    path('delete_person/<int:persona_dni>/', views.delete_person, name='delete_person'),
]
