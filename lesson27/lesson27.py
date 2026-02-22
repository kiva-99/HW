import os
#работа с аргументами и деволтовыми значениями
name = "world"
def greet(name = "world"):
    print(f"hello {name}")
greet("Dima")    
greet()    

def print_args (*args):
    for arg in args:
        print(arg)
print_args(1,2,3)
print_args("a","b","c") 

#функция сложения
def sum(a,b):
    return a+b
result = sum(4,5)
print (result)

#функция факториал
def fuct(x):
    if x ==0:
        return 1
    else:
        return x *fuct(x-1)
print(fuct(5))

#функция лямда

sq = lambda n: n**2
print (sq(5))

#каждый элемент списка в квадрате
list_1 = [1,2,3]
sqs = map (lambda n: n**2, list_1)
print (list(sqs))


a = 5
def my_func():
    global a
    a = 10
    print(a)    
my_func()
print(a)

#рабоиа с файлами и директорией

with open ("hello world.txt", "r") as f:
    content = f.read()
    print (content)

with open ("hello world.txt", "w") as f:
    f.write ("im devops")

with open ("hello world.txt", "a") as f:
    f.write ("im")    

with open ("hello world.txt", "r") as f:
    content = f.read()
    print (content)  


#f not os.path.exists("./lesson27"):
#    os.mkdir("hello") 

if os.path.exists("./lesson27"):
    os.mkdir("lesson27test")
else:
    print("dir n")
