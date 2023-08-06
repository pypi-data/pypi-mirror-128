
import inspect
from .InteractionText import ComponentsText
from .InteractionText import SelectText
from .InteractionText import UserCommandText
from .InteractionText import MsgCommandText
from .SlashCommand import SlashCommand
from .InteractionText import SlashCommandText
from discord.http import Route
from importlib import import_module

class InteractionClient:
    def __init__(self, bot):
        self.bot = bot
        self.appId = None
        self._buttonListeners = {}
        self._selectListeners = {}
        self._userListeners = {}
        self._msgListeners = {}
        self._slashListeners = {}

        self.bot.add_listener(self.__Buttonlistener, 'on_socket_response')
        self.bot.add_listener(self.__Selectlistener, 'on_socket_response')
        self.bot.add_listener(self.__Userlistener, 'on_socket_response')
        self.bot.add_listener(self.__Msglistener, 'on_socket_response')
        self.bot.add_listener(self.__Slashlistener, 'on_socket_response')

    def load_Cog(self, name):
        packge = import_module(name)
        packge.setup(self)

    async def __Buttonlistener(self, load: dict):

        if not self.appId:
            app = await self.bot.application_info()
            self.appId = app.id        

        if load["t"] == "INTERACTION_CREATE" and load.get("d", {}).get("type") == 3:
            data = load["d"]
            if str(data["data"]["component_type"]) == "2":
                await self.__Buttonemit(data["data"]["custom_id"], data)

    async def __Selectlistener(self, load: dict):
        if load["t"] == "INTERACTION_CREATE" and load.get("d", {}).get("type") == 3:
            data = load["d"]
            if str(data["data"]["component_type"]) == "3":
                await self.__Selectemit(data["data"]["custom_id"], data)

    async def __Userlistener(self, load: dict):
        if load["t"] == "INTERACTION_CREATE" and load.get("d", {}).get("type") == 2:
            data = load["d"]
            if str(data["data"]["type"]) == "2":
                await self.__Useremit(data["data"]["name"], data)

    async def __Msglistener(self, load: dict):
        if load["t"] == "INTERACTION_CREATE" and load.get("d", {}).get("type") == 2:
            data = load["d"]
            if str(data["data"]["type"]) == "3":
                await self.__Msgemit(data["data"]["name"], data)

    async def __Slashlistener(self, load: dict):
        if load["t"] == "INTERACTION_CREATE" and load.get("d", {}).get("type") == 2:
            data = load["d"]
            if str(data["data"]["type"]) == "1":
                await self.__Slashemit(data["data"]["name"], data)            

    # 버튼 데코레이터 수집
    def buttonClick(self, custom_id=None):
        def Rdecorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("callback must be a coroutine")

            if custom_id:
                self.__add_listener("button",custom_id, func)
            else:
                self.__add_listener("button",func.__name__, func)

            def Run(*args,**kwargs):
                func(*args,**kwargs)
            return Run
        return Rdecorator

    # 메뉴 데코레이터 수집
    def selectClick(self, custom_id=None):
        def Rdecorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("callback must be a coroutine")

            if custom_id:
                self.__add_listener("menu", custom_id, func)
            else:
                self.__add_listener("menu", func.__name__, func)

            def Run(*args,**kwargs):
                func(*args,**kwargs)
            return Run
        return Rdecorator

    # 유저 커맨드 데코레이터 수집
    def userCommand(self, name=None):
        def Rdecorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("callback must be a coroutine")

            if name:
                self.__add_listener("user", name, func)
            else:
                self.__add_listener("user", func.__name__, func)

            def Run(*args,**kwargs):
                func(*args,**kwargs)
            return Run
        return Rdecorator

    # 메시지 커맨드 데코레이터 수집
    def msgCommand(self, name=None):
        def Rdecorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("callback must be a coroutine")

            if name:
                self.__add_listener("msg", name, func)
            else:
                self.__add_listener("msg", func.__name__, func)

            def Run(*args,**kwargs):
                func(*args,**kwargs)
            return Run
        return Rdecorator    

    # 슬래쉬 커맨드 데코레이터 수집
    def slashCommand(self, name=None):
        def Rdecorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("callback must be a coroutine")

            if name:
                self.__add_listener("slash", name, func)
            else:
                self.__add_listener("slash", func.__name__, func)

            def Run(*args,**kwargs):
                func(*args,**kwargs)
            return Run
        return Rdecorator 

    # 리스너 추가 
    def __add_listener(self, type, event, func):
        if type == "button":
            self._buttonListeners[event] = [func]
        elif type == "menu":
            self._selectListeners[event] = [func]
        elif type == "user":
            self._userListeners[event] = [func]
        elif type == "msg":
            self._msgListeners[event] = [func]
        elif type == "slash":
            self._slashListeners[event] = [func]

    # 버튼 컴포넌트 실행 부
    async def __Buttonemit(self, event, data):
        comp = await (ComponentsText(self.bot)).from_json(data)
        if event in self._buttonListeners:
            for i in self._buttonListeners[event]:
                await i(comp)

    # 메뉴 컴포넌트 실행 부
    async def __Selectemit(self, event, data):
        comp = await (SelectText(self.bot)).from_json(data)
        if event in self._selectListeners:
            for i in self._selectListeners[event]:
                await i(comp)

    # 유저 커맨드 실행 부
    async def __Useremit(self, event, data):
        comp = await (UserCommandText(self.bot)).from_json(data)
        if event in self._userListeners:
            for i in self._userListeners[event]:
                await i(comp)

    # 메시지 커맨드 실행 부
    async def __Msgemit(self, event, data):
        comp = await (MsgCommandText(self.bot)).from_json(data)
        if event in self._msgListeners:
            for i in self._msgListeners[event]:
                await i(comp)

    # 슬래쉬 커맨드 실행 부
    async def __Slashemit(self, event, data):
        comp = await (SlashCommandText(self.bot)).from_json(data)
        if event in self._slashListeners:
            for i in self._slashListeners[event]:
                await i(comp)

    # User Command 추가 요청
    async def add_userCommand(self, name, guild=None):
        
        ids = []

        if guild:
            for id in guild:

                route = Route("POST", f"/applications/{self.appId}/guilds/{id}/commands")
                route.url = f"https://discord.com/api/v9/applications/{self.appId}/guilds/{id}/commands"

                data = {
                    "name": name,
                    "type": 2 
                }

                result = await self.bot.http.request(route, json=data)  
                result = dict(result)
                ids.append(result.get("id"))

        else:
            route = Route("POST", f"/applications/{self.appId}/commands")
            route.url = f"https://discord.com/api/v9/applications/{self.appId}/commands"

            data = {
                "name": name,
                "type": 2 
            }

            result = await self.bot.http.request(route, json=data)  
            result = dict(result)
            ids.append(result.get("id"))      

        return ids

    # Msg Command 추가 요청
    async def add_msgCommand(self, name, guild=None):
        ids = []

        if guild:
            for id in guild:

                route = Route("POST", f"/applications/{self.appId}/guilds/{id}/commands")
                route.url = f"https://discord.com/api/v9/applications/{self.appId}/guilds/{id}/commands"

                data = {
                    "name": name,
                    "type": 3
                }

                result = await self.bot.http.request(route, json=data)  
                result = dict(result)
                ids.append(result.get("id"))

        else:
            route = Route("POST", f"/applications/{self.appId}/commands")
            route.url = f"https://discord.com/api/v9/applications/{self.appId}/commands"

            data = {
                "name": name,
                "type": 3 
            }

            result = await self.bot.http.request(route, json=data)  
            result = dict(result)
            ids.append(result.get("id"))      

        return ids

    async def remove_Command(self, id, guild=None):

        if guild:

            route = Route("DELETE", f"/applications/{self.appId}/guilds/{guild}/commands/{id}")
            route.url = f"https://discord.com/api/v9/applications/{self.appId}/guilds/{guild}/commands/{id}"

            await self.bot.http.request(route)

        else:

            route = Route("DELETE", f"/applications/{self.appId}/commands/{id}")
            route.url = f"https://discord.com/api/v9/applications/{self.appId}/commands/{id}"

            await self.bot.http.request(route)

    async def add_slashCommand(self, slash: SlashCommand, guild=None):
        
        ids = []

        if guild:
            for id in guild:

                route = Route("POST", f"/applications/{self.appId}/guilds/{id}/commands")
                route.url = f"https://discord.com/api/v9/applications/{self.appId}/guilds/{id}/commands"

                data = slash.to_dict()

                result = await self.bot.http.request(route, json=data)  
                result = dict(result)
                ids.append(result.get("id"))

        else:
            route = Route("POST", f"/applications/{self.appId}/commands")
            route.url = f"https://discord.com/api/v9/applications/{self.appId}/commands"

            data = slash.to_dict()

            result = await self.bot.http.request(route, json=data)  
            result = dict(result)
            ids.append(result.get("id"))      

        return ids

    async def sendButton(self, channel, components, content=None, embed=None):
        Components = {}

        if content:
            Components["content"] = content
        elif embed:
            Components["embed"] = embed.to_dict()

        buttons = [{
            "type": 1,
            "components": [
                
            ]    
        }]    

        for i in components:
            buttons[0]["components"].append(i.to_dict()) 

        Components["components"] = buttons 

        await self.bot.http.request(Route(
                        "POST", "/channels/{channel_id}/messages", channel_id=channel
                    ), json=Components)  

    async def sendSelectMenu(self, channel=None, custom_id=None, options=None, placeholder=None, min=None, max=None, content=None, embed=None):
        Components = {}

        if content:
            Components["content"] = content
        elif embed:
            Components["embed"] = embed.to_dict()

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

        for i in options:
            meuns[0]["components"][0]["options"].append(i.to_dict())
        
        Components["components"] = meuns

        await self.bot.http.request(Route(
                        "POST", "/channels/{channel_id}/messages", channel_id=channel
                    ), json=Components) 
