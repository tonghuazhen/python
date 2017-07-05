def calc_sum(*args):
    ax=0
    for n in args:
        ax +=n
    print(ax)
    return ax
calc_sum(1,2,3,4,5)

def lazy_sum(*args):
    def sum():
        ax=0
        for n in args:
            ax+=n
        print(ax)
        return ax
    return sum
f1=lazy_sum(1,2,3,4,5)
print(f1)
f1()

def count():
    def f(j):
        def g():
            print (j*j)
            return j*j
        return g
    fs=[]
    for i in range(1,4):
        fs.append(f(i))
    print(fs)
    return fs

f1,f2,f3=count()
f1()
f2()
f3()

import time
def now():
    print(time.time())
f=now
f()
print(f.__name__)

# decorator
def log(func):
    def wrapper(*args,**kw):
        print("call %s" % func.__name__)
        return func(*args,**kw)
    return wrapper

@log
def hello(name):
    print("hello %s" % name)
hello("sd")
