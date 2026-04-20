from django.urls import path
from . import views

urlpatterns = [

    path('expenses/', views.expense_list_create),
    path('expenses/<int:pk>', views.expense_detail),

    path('categories/', views.category_list),
    path('summary/', views.expense_summary)
]