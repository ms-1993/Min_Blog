from Blog import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.About, name='about'),
    path('blog/', views.BlogListView.as_view(), name='profile'),
    path('create/', views.BlogCreateView.as_view(), name='post_create'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='post_delete'),
    path('update/<int:pk>/', views.BlogUpdateView.as_view(), name='post_update'),
    path('signup/', views.signup, name='signup')
]
