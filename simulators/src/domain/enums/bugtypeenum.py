import enum


class BugTypeEnum(enum.Enum):
    noise = 1
    zero_drop = 2
    wander = 3
    cutoff = 4

    @classmethod
    def get_by_str(cls, bug_type_str: str):
        if bug_type_str is None:
            return None
        else:
            try:
                return BugTypeEnum[bug_type_str]
            except:
                print("Tipo no soportado")
                return None
