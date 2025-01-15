def is_class(any):
    return isinstance(any, type)
def TreeObject(obj: object, objname: str = "", _depth: int = 0):
    if objname != "": print(objname)
    dirobj = dir(obj)
    maxi = len(dirobj) - 1
    for i, attr in enumerate(dirobj):
        attrobj = getattr(obj, attr)
        istype = False # Micropython Bug: if attrobj is type, it will throw Guru Meditation Error
        # print("Attribute: ", attr, "   IsType: ", istype)
        print('|' * _depth + ("├" if i < maxi else "└") + attr + " -- " + (str(type(attrobj)) if istype else "<class \"type\">"))
        if is_class(attrobj) and not istype:
            TreeObject(getattr(obj, attr), "", _depth + 1)

class A:
    a = 1
    b = 5.4
    c = "string"
    def d():
        pass
    class B:
        q = [1,2,3]

TreeObject(A, "A")
