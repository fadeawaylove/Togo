class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class SingletonClass(metaclass=Singleton):
    pass



x = SingletonClass()
y = SingletonClass()
print(x is y)


class SingletonDemo(object):
    class_instance = None
    is_init =False

    def __init__(self, *args, **kwargs):
        if self.is_init is False:
            self.a = 10
            self.b = 20
            self.is_init = True


    def __new__(cls, *args, **kwargs):
        if not cls.class_instance:
            cls.class_instance = super().__new__(cls)
        return cls.class_instance
        
m = SingletonDemo()
n = SingletonDemo()

print(m is n)