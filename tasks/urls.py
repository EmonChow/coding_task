from django.contrib import admin
from django.urls import path
from tasks.views import (
    home,
    login,
    signup,
    addtodo,
    logout,
    search,
    deletetask,
    changetask,
    filter,
    description,
    adminpanel,
    adminwatch,
    admindescription,
    adminedit,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("login", login, name="login"),
    path("signup", signup),
    path("logout", logout, name="logout"),
    path("adminpanel", adminpanel, name="adminpanel"),
    path("adminwatch/<int:id>", adminwatch, name="adminwatch"),
    path("admindescription/<int:id>", admindescription, name="admindescription"),
    path("admin-edit/<str:condition>/<int:id>/<int:user>", adminedit, name="adminedit"),
    path("addtodo", addtodo),
    path("search", search, name="search"),
    path("delete-task/<int:id>", deletetask, name="delete-task"),
    path("change-task/<int:id>/<str:status>", changetask, name="changetask"),
    path("filter/<str:condition>", filter, name="filter"),
    path("description/<int:id>", description, name="description"),
]
