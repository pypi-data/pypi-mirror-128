class SelectOption:
    
    def __init__(self, label=None, value=None, description=None):
        self.label = label
        self.value = value
        self.description = description

    def to_dict(self):
        return {
            "label": self.label,
            "value": self.value,
            "description": self.description
        }
