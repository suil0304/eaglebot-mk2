from library.objects.BaseButt import *
from discord.ext.commands import Bot
from discord.ui import Button

class ArrowButt(BaseButt):
    def __init__(
        self,
        originalInteraction:Interaction,
        timeout:float = 180,
        /,
        *,
        left:BaseButtContent,
        middle:BaseButtContent = DISABLE_BUTT,
        right:BaseButtContent,
    ):
        super().__init__(originalInteraction, timeout)
        
        # callback
        self.leftCallback:BUTT_CALLBACK_TYPE
        self.middleCallback:BUTT_CALLBACK_TYPE = nothingCallback
        self.rightCallback:BUTT_CALLBACK_TYPE
        
        # button
        leftButt:Button = Button(label=left['label'], row=left['row'], style=left['style'], disabled=left['disable'])
        self.add_item(leftButt)
        leftButt.callback = self.left_callback
        self.leftButt:Button = leftButt
        
        middleButt:Button = Button(label=middle['label'], row=middle['row'], style=middle['style'], disabled=middle['disable'])
        self.add_item(middleButt)
        middleButt.callback = self.middle_callback
        self.middleButt:Button = middleButt
        
        rightButt:Button = Button(label=right['label'], row=right['row'], style=right['style'], disabled=right['disable'])
        self.add_item(rightButt)
        rightButt.callback = self.right_callback
        self.rightButt:Button = rightButt
        
    async def left_callback(self, interaction:Interaction):
        if self.leftCallback == None:
            return
        
        await self.leftCallback(interaction)
        
    async def middle_callback(self, interaction:Interaction):
        if self.middleCallback == None:
            return
        
        await self.middleCallback(interaction)
        
    async def right_callback(self, interaction:Interaction):
        if self.rightCallback == None:
            return
        
        await self.rightCallback(interaction)
        