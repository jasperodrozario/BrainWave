from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RoomForm
from .models import Room, Topic, Message
from urllib.parse import unquote_plus

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend Developers'},
#     {'id':4, 'name':'Backend Developers'},
# ]

def loginUser(request):
  page = 'login'
  context = {'page': page}

  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    username = request.POST.get('username').lower()
    password = request.POST.get('password')

    if username == '' or password == '':
      messages.error(request, "Fields cannot be empty.")
      return render(request, 'base/login_form.html', context)
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, "Username does not exist. Sign up to create a new account.")
      return render(request, 'base/login_form.html', context)
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Incorrect username or password.')
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
      if 'password2' in form.errors:
        messages.error(request, "*"+form.errors['password2'])
      elif 'username' in form.errors:
        messages.error(request, "*"+form.errors['username'])
      else:
        messages.error(request, "*"+form.errors)

  return render(request, 'base/login_form.html', context)

def home(request):
  total_room_count = Room.objects.count()
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  if len(q)>0 and ' ' in q[-1]:
    q = q.replace(' ', '+')
  print(q)
  rooms = Room.objects.filter(
    Q(topic__name__icontains = q) | 
    Q(name__icontains = q) | 
    Q(description__icontains = q)
  )
  room_count = rooms.count()

  if q == '':
    selected_topic = ''
  else:
    selected_topic = Topic.objects.filter(
      Q(name__icontains = q)
    )
    if selected_topic.count() == 1:
      selected_topic = selected_topic[0].name
    else:
      selected_topic = None
  print(selected_topic)

  #filtering messages based on queried rooms
  filtered_room_messages = []
  for room in rooms:
    room_messages = Message.objects.filter(room=room)
    filtered_room_messages.extend(room_messages)
  filtered_room_messages.sort(key=lambda event: event.created, reverse=True)

  topics = Topic.objects.all()
  isHomePage = True
  context = {'rooms': rooms, 'topics': topics, 'total_room_count': total_room_count, 'room_count': room_count, 'room_messages': filtered_room_messages, 'flag': isHomePage, 'selected_topic': selected_topic,}
  return render(request, 'base/home.html', context)

def room(request, pk):
  room = Room.objects.get(id=pk)
  participants = room.participants.all()
  participant_count = participants.count()
  if request.method == 'POST':
    Message.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('message_box')
    )
    room.participants.add(request.user)
    return redirect('room', pk=room.id)
  
  room_messages = room.message_set.order_by('updated', 'created')
  context = {'room': room, 'room_messages': room_messages, 'participants': participants, 'participant_count': participant_count}
  return render(request, 'base/room.html', context)

def userProfile(request, pk):
  user = User.objects.get(id=pk)
  user_rooms = user.room_set.all()
  room_count = user_rooms.count()
  room_messages = user.message_set.all()
  isHomePage = False
  context = {'user': user, 'rooms': user_rooms, 'room_messages': room_messages, 'room_count': room_count, 'flag': isHomePage}
  return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
  form = RoomForm()
  context = {'form': form, 'create_page': True}
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid:
      room = form.save(commit=False)
      room.host = request.user
      room.save()
      return redirect('home')
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  context = {'form':form, 'room': room}
  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid:
      form.save()
      return redirect('home')
  return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
  message = Message.objects.get(id=pk)
  if request.method == 'POST':
    message.delete()
    return redirect('room', pk=message.room.id)
  return render(request, 'base/delete.html', {'obj': message})
