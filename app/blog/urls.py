from django.urls import path

from blog import views


app_name = 'blog'

urlpatterns = [
    path('', views.ListBlogApiView.as_view(), name='blogs'),
    path('create/', views.CreateBlogApiView.as_view(), name='create'),
    path('<slug:slug>/',
         views.DetailUpdateDeleteBlogApiView.as_view(),
         name='detail'
         ),
    path('category/list/',
         views.CreateBlogApiView.as_view(),
         name='category_blog'
         ),
    path('category/<slug:slug>/',
         views.ListCategoryApiView.as_view(),
         name='category_list'
         ),
    path('like/<int:pk>/', views.BlogLikeApiView.as_view(), name='like'),
]
