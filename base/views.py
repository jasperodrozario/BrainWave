from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RoomForm
from .models import Room, Topic, Message

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend Developers'},
#     {'id':4, 'name':'Backend Developers'},
# ]

def loginUser(request):
  page = 'login'

  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    username = request.POST.get('username').lower()
    password = request.POST.get('password')
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, "Username does not exist. Sign up to create a new account.")
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Incorrect username or password.')
  context = {'page': page}
  return render(request, 'base/login_form.html', context)

def logoutUser(request):
  logout(request)
  return redirect('home')

def registerUser(request):
  form = UserCreationForm()
  context = {'form': form}
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Something went wrong. Please try again.')
  return render(request, 'base/login_form.html', context)

def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(
    Q(topic__name__icontains = q) | 
    Q(name__icontains = q) | 
    Q(description__icontains = q)
  )
  room_count = rooms.count()

  #filtering messages based on queried rooms
  filtered_room_messages = []
  for room in rooms:
    room_messages = Message.objects.filter(room=room)
    filtered_room_messages.extend(room_messages)
  filtered_room_messages.sort(key=lambda event: event.created, reverse=True)

  topics = Topic.objects.all()
  context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': filtered_room_messages}
  return render(request, 'base/home.html', context)

def room(request, pk):
  room = Room.objects.get(id=pk)
  participants = room.participants.all()

  if request.method == 'POST':
    Message.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('message_box')
    )
    room.participants.add(request.user)
    return redirect('room', pk=room.id)
  
  room_messages = room.message_set.all()
  context = {'room': room, 'room_messages': room_messages, 'participants': participants}
  return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
  form = RoomForm()
  context = {'form': form}
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid:
      form.save()
      return redirect('home')
  return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  context = {'form':form}
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid:
      form.save()
      return redirect('home')
  return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj':room})

def deleteMessage(request, pk):
  message = Message.objects.get(id=pk)
  if request.method == 'POST':
    message.delete()
    return redirect('room', pk=message.room.id)
  return render(request, 'base/delete.html', {'obj': message})
