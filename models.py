from django.db import models

# Create your models here.
class Websites(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

        verbose_name = "网址"
        verbose_name_plural = "网址"

    def __str__(self):
        return f"{self.name}: {self.url}"