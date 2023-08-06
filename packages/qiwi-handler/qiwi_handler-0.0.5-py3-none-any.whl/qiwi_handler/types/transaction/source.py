
class Source:
    def __init__(self, source = None):
        self.source = source


    def __str__(self):
        return str(self.__dict__)