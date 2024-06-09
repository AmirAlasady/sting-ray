from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class Conversation(models.Model):
    title=models.CharField(max_length=30)
    user_owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='its_conversations')
    start_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Chat(models.Model):
    query = models.CharField(max_length=1000000)
    answer = models.CharField(max_length=1000000)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,related_name='its_chats')
    options=(
        ('s','system'),
        ('n','normal'),
        ('c','controll'),
        ('r','rag')
    )
    chat_type=models.CharField(max_length=30,choices=options,default='n')
    def __str__(self):
        return f'conv: {self.conversation} | Query: {self.query} | Answer: {self.answer}'
    



def validate_file_extension(value):
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    if not any(value.name.lower().endswith(ext) for ext in allowed_extensions):
        raise ValidationError(f"Unsupported file type. Only PDFs (.pdf), DOCX (.docx), or DOC (.doc) files are allowed.")

class Files_data(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[validate_file_extension],blank=True, null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='its_files')
    options=(
        ('f','false'),
        ('t','true'),
    )
    is_read=models.CharField(max_length=30,choices=options,default='f')

    """
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
            super().save(*args, **kwargs)
    """    

    def __str__(self):
        return f'conv: {self.conversation} | file: {self.file.name}'

