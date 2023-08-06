class Button:

    def __init__(self, label=None, style=None, custom_id=None, url=None):
        self.lable = label
        self.style = style
        self.custom_id = custom_id
        self.url = url

    def to_dict(self):
        data = {
            "type": 2,
            "label": self.lable,
            "style": self.style,
        }
        if self.style != 5:
            data["custom_id"] = self.custom_id
        else:
            data["url"] = self.url
        return data

class ButtonStyle:

    def __init__(self):
        self.PRIMARY = 1
        self.SECONDARY = 2
        self.SUCCESS = 3
        self.DANGER = 4
        self.LINK = 5