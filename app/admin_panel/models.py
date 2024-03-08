from django.db import models

from accounts.models import User


class UserPageVisitModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    page_url = models.URLField()
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.page_url} - {self.visit_time}"
        return f"Anonymous - {self.page_url} - {self.visit_time}"

