from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action
from chat_app.models import Message, Room
from chat_app.serializers import MessageSerializer, RoomSerializer
from channels.db import database_sync_to_async


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    @action()
    async def create_room(self, message):
        room: Room = await self.get_room(pk=self.room_subscribe)  # noqa
        new_message = await self.save_room_to_db(room, message)
        serialized_message = MessageSerializer(new_message).data
        await self.send_message_to_room(room, serialized_message)  # noqa

    @database_sync_to_async
    def save_room_to_db(self, room, message):
        user = self.scope["user"]
        return Message.objects.create(room=room, user=user, text=message)

    # message in database

    @action()
    async def create_message(self, message, room_id, user_id, to_id):
        room = await self.get_room(pk=room_id)  # noqa
        user = await self.get_user(pk=user_id)  # noqa
        to = await self.get_user(pk=to_id)  # noqa
        new_message = await self.save_message_to_db(room, user, to, message)
        serialized_message = MessageSerializer(new_message).data
        await self.send_message_to_room(room, serialized_message)  # noqa

    @database_sync_to_async
    def save_message_to_db(self, room, user, to, message):
        return Message.objects.create(room=room, user=user, to=to, text=message)
