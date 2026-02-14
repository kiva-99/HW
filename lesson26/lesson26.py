# проверка чётности числа x
x = 7
if x %2 == 0:
    print("число", x, "является четное")
else:
    print("число", x, "является нечетное")
# цикл выводим число a пока оно < 5
print("выводим a пока оно меньше 5")
a = 0
while a < 5:
    print (a)
    a += 1
# работа с циклом for
print ("цикл for")
numbers = [1,2,3]
for i in numbers:
    print(i)

# массивы
print ("массивы")
my_array =[1,2,3,4,5]
print(my_array[0],my_array[2])
print(my_array[0:5])
for i in my_array:
    print(i)
my_array[2]=9
print (my_array)
#
my_array.append(6)
print (my_array)
#
my_array.insert(0,6)
print (my_array)
#
print(len(my_array))

# работа с кортежами
print ("работа с кортежами")
my_tuple = ("devops",5,False)
title, years_in_comp, coder = my_tuple
print (title,years_in_comp)
#
def my_func1():
    return 1,2,3
c,d,e = my_func1()
print (c,d,e)

#словари
print("словари")
my_dict1 = {"fruits": "apples", "veg": ["tomatoes","potatoes","cucumber"]}
print (my_dict1["veg"])
print (my_dict1["veg"][1])
my_dict1["fruits"] = ["apples", "oranges"]
print (my_dict1["fruits"][0:2])

items_list = list(my_dict1.values())
print (items_list)
items_list = list(my_dict1.keys())
print (items_list)
#items_list = list(my_dict1.())
#print (items_list)
#y = 3.14
#name = "Jone"
#my_list = [1,2,3]
#my_tuple = (4,5,6)
#my_dict = {"name": "Jone" , "age": "30"}
#a , b , c = my_tuple
#str1 = "this is"
#values = [1]
#item_list = list(my_dict.items())