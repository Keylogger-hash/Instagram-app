from django.shortcuts import render
from django.contrib.auth.models import User
from chat.models import Room,Message
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def chat(request,label):
    room = Room.objects.get(label=label)
    message = reversed(room.messages.order_by('-date_send')[:50])
    is_message = True
    if room.messages.exists():
        context = {"room":room,"message":message,"is_message":is_message}
    else:
        context = {"room":room,is_message:False}
    return render(request,"chat/chat.html",context=context)


# @login_required
# def new_chat(request):
#     profiles =  request.user.profile.subscribers.all()
#     context = {
#     'profiles':profiles
#     }
#     return render(request,'chat/new_chat.html',context=context)


@login_required
def inbox(request):
    inbox = Room.objects.filter(Q(reciever=request.user)|Q(sender=request.user))
    context = {
    "inbox":inbox
    }
    return render(request,"chat/inbox.html",context=context)


@login_required
def chat_create(request,username):
    user_to_message = User.objects.get(username=username)
    room_label = request.user.username+'_'+user_to_message.username
    does_room_exist = Room.objects.filter(label=room_label)
    if does_room_exist.exists():
        return HttpResponseRedirect(reverse('chat:chat',kwargs={'label':room_label}))
    else:
        room = Room(label=room_label,reciever=user_to_message,sender=request.user)
        room.save()
        return HttpResponseRedirect(reverse('chat:chat',kwargs={'label':room_label}))
