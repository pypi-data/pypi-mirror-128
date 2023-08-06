
class MakeDict:
    def __str__(self):
        dic = {}
        for key in self.__dict__:
            dic[key] = str(self.__dict__[key])

        return str(dic)
