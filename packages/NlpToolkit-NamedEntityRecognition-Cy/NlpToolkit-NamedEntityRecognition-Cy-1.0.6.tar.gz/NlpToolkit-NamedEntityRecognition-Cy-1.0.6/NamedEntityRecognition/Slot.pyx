from NamedEntityRecognition.SlotType import SlotType


cdef class Slot:

    def __init__(self, str tag, type = None):
        if type is not None:
            self.tag = tag
            self.type = type
        else:
            if tag == "O":
                self.type = SlotType.O
                self.tag = ""
            else:
                _type = tag[0:tag.find("-")]
                _tag = tag[tag.find("-") + 1:]
                if _type == "B":
                    self.type = SlotType.B
                elif _type == "I":
                    self.type = SlotType.I
                self.tag = _tag

    cpdef object getType(self):
        return self.type

    cpdef str getTag(self):
        return self.tag

    def __str__(self) -> str:
        if self.type == SlotType.O:
            return "O"
        elif self.type == SlotType.B or self.type == SlotType.I:
            return self.type.name + "-" + self.tag
        return ""
