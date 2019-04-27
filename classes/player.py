class Player:
    def __init__(self, id):
        self._id = id
    
    def get_id(self):
        return self._id

    def get_color(self):
        if self._id == 0:
            return (255,0,0)
        else:
            return (255,255,0)

    def get_name(self):
        if self._id == 0:
            return "Red"
        else:
            return "Yellow"