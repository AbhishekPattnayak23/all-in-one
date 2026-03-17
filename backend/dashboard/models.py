from django.db import models

class DashboardMetric(models.Model):
    total_users = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dashboard metric at {self.created_at}"
