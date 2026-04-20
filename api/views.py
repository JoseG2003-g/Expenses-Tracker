from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category, Expense
from .serializer import CategorySerializer, ExpenseSerializer
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.models import User
import pandas as pd
# Create your views here.

@api_view(['GET', 'POST'])
def expense_list_create(request):

    if request.method == 'GET':
        expenses = Expense.objects.all().order_by('-created_at')
        serializer = ExpenseSerializer(expenses, many=True)
        return Response (serializer.data)
    
    if request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.first()
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'POST'])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response (serializer.data)
    
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def expense_summary(request):
   user = User.objects.first()

   current_month = datetime.now().month

   expenses = Expense.objects.filter(
       user = user, 
       created_at__month = current_month

   )

   total = expenses.aggregate(total=Sum('amount'))['total'] or 0
   by_category = expenses.values('category__name').annotate(total=Sum('amount'))  

   formatted = {
       item['category__name']: item['total']
       for item in by_category
   }    

   return Response({
       
       "total": total,
       "by_category": formatted
   })                   
                                  
                                  
        
    