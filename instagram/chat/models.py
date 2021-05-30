from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Room(models.Model):
    label = models.SlugField(unique=True)
    sender = models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE)
    reciever = models.ForeignKey(User,related_name='reciever',on_delete=models.CASCADE)

    def get_last_message(self):
        message = Message.objects.filter(room=self.id).last()
        if message is None:
            return ""
        else:
            return message.text


class Message(models.Model):
    room = models.ForeignKey(Room,related_name="messages",on_delete=models.CASCADE)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    date_send = models.DateTimeField(default=datetime.now,db_index=True)
