from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Purchase
from .serializers import ProjectSerializer, PurchaseSerializer
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from pypaystack2 import Paystack
import uuid

paystack = Paystack(auth_key=settings.PAYSTACK_SECRET_KEY)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def initiate_purchase(self, request, pk=None):
        project = self.get_object()
        user = request.user

        if not project.is_paid:
            return Response({"error": "This project is free and doesn't require purchase."}, status=status.HTTP_400_BAD_REQUEST)

        if Purchase.objects.filter(user=user, project=project).exists():
            return Response({"error": "You have already purchased this project."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Paystack transaction
        amount_in_kobo = int(project.price * 100)  # Convert to kobo (Paystack uses the smallest currency unit)
        callback_url = request.build_absolute_uri(reverse('project-verify-payment', kwargs={'pk': project.id}))
        
        try:
            response = paystack.transaction.initialize(
                email=user.email,
                amount=amount_in_kobo,
                callback_url=callback_url
            )
            return Response({"payment_url": response['data']['authorization_url']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def verify_payment(self, request, pk=None):
        project = self.get_object()
        user = request.user
        reference = request.GET.get('reference')

        if not reference:
            return Response({"error": "No reference provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = paystack.transaction.verify(reference)
            if response['status'] and response['data']['status'] == 'success':
                # Payment successful, create purchase
                purchase = Purchase.objects.create(
                    user=user,
                    project=project,
                    transaction_id=reference
                )

                # Generate download link
                download_link = request.build_absolute_uri(reverse('project-download', kwargs={'pk': project.id}))

                # Send email with download link
                send_mail(
                    'Your Project Download',
                    f'Thank you for your purchase. You can download your project here: {download_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                return Response({"message": "Payment verified. Check your email for the download link."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        project = self.get_object()
        user = request.user

        if not project.is_paid or Purchase.objects.filter(user=user, project=project).exists():
            if project.file:
                file_path = project.file.path
                return Response({"download_url": file_path}, status=status.HTTP_200_OK)
            elif project.file_url:
                return Response({"download_url": project.file_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No file available for download."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "You need to purchase this project before downloading."}, status=status.HTTP_403_FORBIDDEN)

class PurchaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)
















# from rest_framework import viewsets, permissions, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Project, Purchase
# from .serializers import ProjectSerializer, PurchaseSerializer
# from django.shortcuts import get_object_or_404
# from django.core.mail import send_mail
# from django.conf import settings
# import uuid

# class ProjectViewSet(viewsets.ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
#     def purchase(self, request, pk=None):
#         project = self.get_object()
#         user = request.user

#         if not project.is_paid:
#             return Response({"error": "This project is free and doesn't require purchase."}, status=status.HTTP_400_BAD_REQUEST)

#         if Purchase.objects.filter(user=user, project=project).exists():
#             return Response({"error": "You have already purchased this project."}, status=status.HTTP_400_BAD_REQUEST)

#         # Here, you would typically integrate with Paystack for payment processing
#         # For this example, we'll simulate a successful payment

#         transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID
#         purchase = Purchase.objects.create(user=user, project=project, transaction_id=transaction_id)

#         # Generate download link
#         download_link = request.build_absolute_uri(f'/api/portfolio/projects/{project.id}/download/')

#         # Send email with download link
#         send_mail(
#             'Your Project Download',
#             f'Thank you for your purchase. You can download your project here: {download_link}',
#             settings.EMAIL_HOST_USER,
#             [user.email],
#             fail_silently=False,
#         )

#         return Response({"message": "Purchase successful. Check your email for the download link."}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
#     def download(self, request, pk=None):
#         project = self.get_object()
#         user = request.user

#         if not project.is_paid or Purchase.objects.filter(user=user, project=project).exists():
#             if project.file:
#                 file_path = project.file.path
#                 return Response({"download_url": file_path}, status=status.HTTP_200_OK)
#             elif project.file_url:
#                 return Response({"download_url": project.file_url}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "No file available for download."}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"error": "You need to purchase this project before downloading."}, status=status.HTTP_403_FORBIDDEN)

# class PurchaseViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = PurchaseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Purchase.objects.filter(user=self.request.user)