from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, PurchaseViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'purchases', PurchaseViewSet, basename='purchase')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:pk>/verify-payment/', ProjectViewSet.as_view({'get': 'verify_payment'}), name='project-verify-payment'),
]

