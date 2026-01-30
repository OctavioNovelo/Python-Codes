# **********************************************************************
print("\n***********************************************************\n")
# **********************************************************************
# Functions

def suma(a, b, c):
    return a + b + c

print(type(suma))

print(suma(2, 3, 5))

# **********************************************************************
print("\n***********************************************************\n")
# **********************************************************************

def printName(firstName, lastName):
    print(f'{lastName}, {firstName}')

printName()
printName('Jaime')
printName('Jaime', 'Estrella')

printName(lastName='Estrella', firstName='Jaime')

printName(lastName='Estrella')

# **********************************************************************
print("\n***********************************************************\n")
# **********************************************************************

x = 10 #Variable Global

def fx():
    global x #Acceso a la variable global
    #Variable local
    x = 15
    print(x)

fx()
print(x)

