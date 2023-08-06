class SlashCommand:
    
    def __init__(self, name=None, description=None, options=None, subCommand=None):
        self.name = name
        self.description = description

        if subCommand:
            self.subCommand = subCommand
        
        if options:
            self.options = options
        
    def to_dict(self):
        data = {
            "name": self.name,
            "type": 1,
            "description": self.description,
            "options": [

            ]
        }

        if self.options:
            for value in self.options:
                data["options"].append(value.to_dict())

        return data        

class ArgumentType:

    def __init__(self):
        self.SUB_COMMAND = 1
        self.SUB_COMMAND_GROUP = 2
        self.STRING = 3
        self.INTEGER = 4
        self.BOOLEAN = 5
        self.USER = 6
        self.CHANEEL = 7
        self.ROLE = 8
        self.MENTIONABLE = 9
        self.NUMBER = 10

class Argument:

    def __init__(self, name=None, description=None, choices=None, type=None, required:bool=None):
        self.name = name
        self.description = description
        self.required = required
        self.type = type
        self.choices = choices     

    def to_dict(self):
        data = {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "required": self.required,
        }        

        if self.choices != None:
            data["choices"] = [

            ]

            for value in self.choices:
                data["choices"].append({
                    "name": value.name,
                    "value": value.value
                }) 

        return data

class Choices:

    def __init__(self, name, value):
        self.name = name
        self.value = value        
