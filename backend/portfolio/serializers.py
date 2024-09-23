from rest_framework import serializers
from .models import Project, Purchase

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tags', 'price', 'image', 'is_paid', 'created_at', 'updated_at']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'project', 'purchase_date', 'transaction_id']