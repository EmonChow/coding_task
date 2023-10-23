from django.urls import path

from tasks import todo_task_views as views

urlpatterns = [
	path('api/v1/todo/all/', views.getAlltodo),
 
    path('api/v1/todo/all/without_pagination/', views.getAlltodoWithoutPagination),

	path('api/v1/todo/<int:pk>', views.getAtodo),

	path('api/v1/todo/create/', views.createtodo),

	path('api/v1/todo/update/<int:pk>', views.updatetodo),
	
	path('api/v1/todo/delete/<int:pk>', views.deletetodo),
]
