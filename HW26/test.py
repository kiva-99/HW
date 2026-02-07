# типы переменных
print("hello word")
print (type (2)) #int
print (type ('2')) #str
print (type (2.0)) #flor
#операции с переменными для чисел
x=1
y=4
z=x+y
print (z)
z1=y-x
print (z1)
print (x*y)
print (x/y)
print (x**y)
print (y//x)
print (x%y)
print ((x+y)-(x*y))
# условные операторы
print ("работа с условными операторами")
a = 20
if a < 10:
    print ("a < 10")
else:
    print ("a >= 10")    
print ("работа с циклами for")

for i in range (9):
    print (i)

print ("работа с функциями func")

def function_test (d,e):
    return d+e
print (function_test(21,38))