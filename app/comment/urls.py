from django.urls import path

from comment import views


app_name = 'comment'

urlpatterns = [
    path('<int:pk>/', views.ListCommentApiView.as_view(), name='comments'),
    path('create/', views.CreateCommentApiView.as_view(), name='create'),
    path('update-delete/<int:pk>/',
         views.UpdateDeleteCommentApiView.as_view(),
         name='update_delete')
]
