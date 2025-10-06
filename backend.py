# Final enhanced backend.py with Update, Delete, Add, Reset, Get Total, Get All Expenses

import os
import sys
from datetime import datetime
from django.conf import settings
from django.utils.crypto import get_random_string

def configure_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expense_tracker.settings")

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY=get_random_string(50),
            ROOT_URLCONF=__name__,
            ALLOWED_HOSTS=['*'],
            MIDDLEWARE=[
                'corsheaders.middleware.CorsMiddleware',
                'django.middleware.common.CommonMiddleware',
                'django.middleware.security.SecurityMiddleware',
                'django.middleware.csrf.CsrfViewMiddleware',
                'django.middleware.clickjacking.XFrameOptionsMiddleware',
            ],
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'rest_framework',
                'corsheaders',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'expense_tracker.sqlite3',
                }
            },
            REST_FRAMEWORK={
                'DEFAULT_PERMISSION_CLASSES': [],
                'UNAUTHENTICATED_USER': None,
            },
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            }],
            CORS_ALLOW_ALL_ORIGINS=True,
        )

    import django
    django.setup()

# --- Configure Django ---
configure_django()

# --- Django Imports ---
from django.core.wsgi import get_wsgi_application
from django.urls import path
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from db import collection

# --- Serializer ---
class ExpenseSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    amount = serializers.FloatField(min_value=0.01)
    date = serializers.DateTimeField(default=datetime.now)
    category = serializers.CharField(max_length=100, default="Others")

    def create(self, validated_data):
        result = collection.insert_one(validated_data)
        validated_data['_id'] = str(result.inserted_id)
        return validated_data

# --- API Views ---
@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"}, status=200)

@api_view(['GET'])
def get_expenses(request):
    try:
        expenses = list(collection.find({}, {'_id': 1, 'product_name': 1, 'amount': 1, 'category': 1, 'date': 1}))
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
        return Response(expenses)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def add_expense(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        try:
            expense = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_expense(request, expense_id):
    try:
        from bson import ObjectId
        update_fields = request.data
        result = collection.update_one({"_id": ObjectId(expense_id)}, {"$set": update_fields})
        if result.modified_count == 1:
            return Response({"message": "Expense updated successfully"})
        else:
            return Response({"error": "Expense not found or no changes made"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_total_expenses(request):
    try:
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
        result = list(collection.aggregate(pipeline))
        total = result[0]["total"] if result else 0
        return Response({"total": total})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['DELETE'])
def reset_expenses(request):
    try:
        collection.delete_many({})
        return Response({"message": "All expenses deleted successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['DELETE'])
def delete_expense(request, expense_id):
    try:
        from bson import ObjectId
        result = collection.delete_one({"_id": ObjectId(expense_id)})
        if result.deleted_count == 1:
            return Response({"message": "Expense deleted successfully"})
        else:
            return Response({"error": "Expense not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# --- URL Patterns ---
urlpatterns = [
    path('api/health/', health_check, name='health_check'),
    path('api/expenses/', get_expenses, name='get_expenses'),
    path('api/expenses/add/', add_expense, name='add_expense'),
    path('api/expenses/<str:expense_id>/update/', update_expense, name='update_expense'),
    path('api/expenses/total/', get_total_expenses, name='get_total_expenses'),
    path('api/expenses/reset/', reset_expenses, name='reset_expenses'),
    path('api/expenses/<str:expense_id>/delete/', delete_expense, name='delete_expense'),
]

application = get_wsgi_application()

# --- Run Server ---
def run_django_server():
    from django.core.management import execute_from_command_line
    port = "8000"
    execute_from_command_line([sys.argv[0], "runserver", f"0.0.0.0:{port}"])

if __name__ == "__main__":
    run_django_server()