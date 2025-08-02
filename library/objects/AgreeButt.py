from library.objects.BaseButt import *
from discord.ext.commands import Bot
from discord.ui import Button

class AgreeButt(BaseButt):
    def __init__(
        self,
        originalInteraction:Interaction,
        timeout:float = 180,
        /,
        *,
        agreeRow:int = 0,
        declineRow:int = 0,
    ):
        super().__init__(originalInteraction, timeout)
        
        # callback
        self.agreeCallback:BUTT_CALLBACK_TYPE
        self.declineCallback:BUTT_CALLBACK_TYPE
        
        # button
        agreeButt:Button = Button(label='✅', row=agreeRow, style=ButtonStyle.success)
        self.add_item(agreeButt)
        agreeButt.callback = self.agree_callback
        self.agreeButt:Button = agreeButt
        
        declineButt:Button = Button(label='🚫', row=declineRow, style=ButtonStyle.danger)
        self.add_item(declineButt)
        declineButt.callback = self.decline_callback
        self.declineButt:Button = declineButt
        
    async def agree_callback(self, interaction:Interaction):
        if self.agreeCallback == None:
            return
        
        await self.agreeCallback(interaction)
        
    async def decline_callback(self, interaction:Interaction):
        if self.declineCallback == None:
            return
        
        await self.declineCallback(interaction)
        