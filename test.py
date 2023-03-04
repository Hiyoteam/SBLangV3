def process(obj):
    obj.value+=1
class obj:
    def __init__(self) -> None:
        self.value=0
OBJ=obj()
process(OBJ)
print(OBJ.value)
