import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class BarConsumer(WebsocketConsumer):
	room_name = 'bar'

	def connect(self):
		# print(">>>>>>>", self.scope)
		# self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'chat_{self.room_name}'
		async_to_sync(self.channel_layer.group_add)(
				self.room_group_name,
				self.channel_name
			)
		self.accept()

	def disconnect(self, close_code):
		# Leave room group
		async_to_sync(self.channel_layer.group_discard)(
				self.room_group_name,
				self.channel_name
			)

	# Recieve message from WebSocket 
	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# Send message to group
		async_to_sync(self.channel_layer.group_send)(
				self.room_group_name,
				{
					'type': 'broadcast',
					'message': message
				}
			)
		# self.send(text_data=json.dumps({
		# 	'message': message
		# }))

	# Receive message from room group
	def broadcast(self, event):
		message = event['message']
		print(">>>>>>>>>>>>", event)
		# Send message to WebSocket
		self.send(text_data=json.dumps({
				'message': message
			}))