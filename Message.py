

class Message:
    
    def __init__(self):
        self.name: str
        self.description: str

    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str):
        self.name = name

    def get_description(self):
        return self.description
    
    def set_description(self, description):
        self.description = description