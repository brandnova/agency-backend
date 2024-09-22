from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.CharField(max_length=500)  # Store as comma-separated values
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    file_url = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='project_files/', blank=True, null=True)
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"