from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    # 名称留空代表即该APP的主页，类似于***.***.***/polls，即可看到
    # name = '***'定义的名称可以在模版中引用，如：{% url '***' %}
    # ex /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex /polls/access
    # path('access', views.access, name='access'),
    # ex /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex /polls/5/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex /polls/5/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
