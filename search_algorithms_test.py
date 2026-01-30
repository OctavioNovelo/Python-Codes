# Lineal Search

#import dtslib
#dtslib.linealSearch(data, element)

#import dtslib as dts
#dts.linealSearch(data, element)

#from dtslib import linealSearch
#linealSearch(data, element)

#from dtslib import linealSearch as ls
#ls(data, element)

from dtslib import *

data = [1, 0, -4, 5, 11, 2, -9, 3, 17, 6]

element = 3

index = linealSearch(data, element)

if index >= 0 :
    print(f'Valor {element} encontrado en {index}')
else:
    print(f'Elemento no encontrao')


# *************************************************************************************
print('\n**************************************************************************\n')
# *************************************************************************************

class Student:
    def __init__(self, name, age, id):
        self.name = name
        self.age = age
        self.id = id

    def __str__(self):
        return f'{self.name}, {self.age}, {self.id}'

data = [
    Student('Pedro Alvares' , 20, '816505'),
    Student('Juan Perez' , 32, '563188'),
    Student('Martha Montejo' , 45, '235474'),
    Student('Laura Cisneros' , 37, '937125'),
    Student('Erick Parra' , 18, '754638'),
]