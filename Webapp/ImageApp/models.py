from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField để tự động tạo id
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField để tự động tạo id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatTurn(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField để tự động tạo id
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    turn_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChatbotMessage(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField để tự động tạo id
    chat_turn = models.ForeignKey(ChatTurn, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    id = models.AutoField(primary_key=True)  # Sử dụng AutoField để tự động tạo id
    chat_turn = models.ForeignKey(ChatTurn, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    prompt_text = models.TextField()
    image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

