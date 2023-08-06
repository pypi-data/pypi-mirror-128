from discord.http import Route
from .Button import Button
from .SelectOption import SelectOption

class InteractionText:

    def __init__(self, bot) -> None:
        self.bot = bot
        self.type = None
        self.user = None
        self.guild = None
        self.channel = None
        self.__token = None
        self.__id = None

    async def from_json(self, data: dict):
        self.type = data.get("type")
        self.__token = data.get("token")
        self.__id = data.get("id")
        self.guild = await self.bot.fetch_guild(int(data.get("guild_id"))) 
        self.channel = await self.bot.fetch_channel(int(data.get("channel_id")))
        self.user = await self.guild.fetch_member(int(data.get("member").get("user").get("id")))

        return self

    async def reply(self, content=None, embed=None, components=None, custom_id=None, placeholder=None, min=None, max=None, hide:bool=None):
        if not content and not embed:
            await self.bot.http.request(
                Route("POST", f"/interactions/{self.__id}/{self.__token}/callback"),
                json={"type": 6}
                )      
            return

        data = {"type": 4, "data": {
                
            }}
        if content:
            data["data"]["content"] = content          
        if embed:
            data["data"]["embeds"] = [embed.to_dict()]
        if hide == True:
            data["data"]["flags"] = 64 
            
        if components:
            if isinstance(components[0], Button):
                buttons = [{
                    "type": 1,
                    "components": [
                        
                    ]    
                }]    

                for i in components:
                    buttons[0]["components"].append(i.to_dict()) 

                data["data"]["components"] = buttons 
            elif isinstance(components[0], SelectOption):   
                if custom_id:
                    if placeholder:
                        if min:
                            if max:
                                meuns = [{
                                    "type": 1,
                                    "components": [
                                        {
                                            "type": 3,
                                            "custom_id": custom_id,
                                            "placeholder": placeholder,
                                            "min_values": min,
                                            "max_values": max,
                                            "options": [

                                            ]
                                        }
                                    ]    
                                }]    

                                for i in components:
                                    meuns[0]["components"][0]["options"].append(i.to_dict())
                                
                                data["data"]["components"] = meuns

        await self.bot.http.request(
            Route("POST", f"/interactions/{self.__id}/{self.__token}/callback"),
            json=data
            ) 

class ComponentsText(InteractionText):

    def __init__(self, bot):
        super().__init__(bot)

    async def from_json(self, data: dict):
       await super().from_json(data)
       self.message = await self.channel.fetch_message(int(data["message"]["id"]))   
       return self

class SelectText(InteractionText):

    def __init__(self, bot):
        super().__init__(bot)                     

    async def from_json(self, data: dict):
        await super().from_json(data)
        self.message = await self.channel.fetch_message(int(data["message"]["id"]))   
        self.selectValues = data.get("data").get("values")
        return self

class MsgCommandText(InteractionText):

    def __init__(self, bot):
        super().__init__(bot)

    async def from_json(self, data: dict):
        await super().from_json(data)    
        self.name = data["data"]["name"]
        self.message = await self.channel.fetch_message(int(data["data"]["target_id"]))
        self.command_id = data["data"]["id"]
        return self

class UserCommandText(InteractionText):

    def __init__(self, bot):
        super().__init__(bot)

    async def from_json(self, data: dict):
        await super().from_json(data)    
        self.name = data["data"]["name"]
        self.target = await self.guild.fetch_member(int(data["data"]["target_id"]))
        self.command_id = data["data"]["id"]
        return self

class SlashCommandText(InteractionText):

    def __init__(self, bot):
        super().__init__(bot)

    async def from_json(self, data: dict):
        await super().from_json(data)    
        self.name = data["data"]["name"]
        self.command_id = data["data"]["id"]
        options = []
        for value in list(data["data"]["options"]):
           options.append(ArgOption(value=value["value"], type=value["type"], name=value["name"]))      
        self.options = options
        return self 

class ArgOption:

    def __init__(self, value, type, name):
        self.value = value
        self.type = type
        self.name = name


