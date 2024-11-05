from django.db import models

class EmailAnalysis(models.Model):
    sender = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    is_phishing = models.BooleanField(default=False)
    confidence_score = models.IntegerField(default=0)  # Add field for confidence score
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {'Phishing' if self.is_phishing else 'Not Phishing'}"
