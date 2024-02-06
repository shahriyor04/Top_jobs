from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse

from chat_app.models import Room, Message


def lobby(request):
    return render(request, 'chat_app/lobby.html')


def room(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name:
            room = Room.objects.create(name=name, host=request.user) # noqa
            return HttpResponseRedirect(reverse("room", args=[room.pk]))
    return render(request, 'chat_app/index.html')


def message(request, pk):
    room = get_object_or_404(Room, pk=pk) # noqa
    messages = Message.objects.filter(room=room).order_by('created_at')
    if request.method == "POST":
        message_text = request.POST.get("message", None)
        if message_text:
            Message.objects.create(room=room, user=request.user, text=message_text)
            return HttpResponseRedirect(reverse("room", args=[room.pk]))

    return render(request, 'chat_app/room.html', {
        "room": room,
        "messages": messages,
    })
