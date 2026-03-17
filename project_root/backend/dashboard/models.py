from django.db import models
class DashboardMetrics(models.Model):
    total_users = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
