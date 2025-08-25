from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    uploaded_file = models.FileField(upload_to="notes/", blank=True, null=True)  # ✅ new field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Summary(models.Model):
    note = models.OneToOneField(Note, on_delete=models.CASCADE, related_name="summary")
    content = models.TextField()

    def __str__(self):
        return f"Summary of {self.note.title}"


class Quiz(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz for {self.note.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'✔' if self.is_correct else '✘'})"


# class Note(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField(blank=True, null=True)
#     uploaded_file = models.FileField(upload_to="notes/", blank=True, null=True)  # ✅ new field
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title