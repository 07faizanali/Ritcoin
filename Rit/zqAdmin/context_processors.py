from wallet.models import CustomCoinRate




def getZQLRate(request):

    # return {'ZQLRate':  CustomCoinRate.objects.get(id=1).amount}
    updatedZaanRate=float(CustomCoinRate.objects.filter(coin_name='ZQL').order_by('-id').first().amount)
    # return {'ZQLRate':  CustomCoinRate.objects.get(id=1).amount}
    return {'ZQLRate':  updatedZaanRate}












# # consumers.py (using Django Channels for WebSocket communication)
# import asyncio
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import Investment

# class ROIConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.update_roi()

#     async def update_roi(self):
#         # Send updates to connected clients every second
#         while True:
#             investments = Investment.objects.all()
#             for investment in investments:
#                 await self.send(text_data=json.dumps({
#                     'user_id': investment.user_id,
#                     'current_return': investment.current_return
#                 }))
#             await asyncio.sleep(1)

#     async def disconnect(self, close_code):
#         pass  # Handle disconnection if needed



