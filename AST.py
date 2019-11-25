##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 3
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 21:16 Hora de Venezuela
##Fecha de modificación: 03-11-2019 en lamañana

##Actualización: Estructura básica de los nodos del AST. ES probable que falten cosas o que no esté del todo bien
#En principio category nos indica la regla que se está aplicando y en value va una tupla (Tipo,valor) donde tio indica el
##tipo de la variable y valor en valor como tal. En algunos casos simplemente hay valor. No estoy muy claro como funcionará
##en operadore

import sys

#Dado un objeto correspondiente a un identificador almacenado en la tabla de símbolos retorna el tipo del identificador.
#En el caso de ser el objeto una instancia de ArrayInfo, simplemente retorna como tipo "array", sin información de los
# límites del mismo 
#Parámetro:
#value: Objeto de la tabla de símbolos. Puede ser str o ArrayInfo
#retorna: int, bool, o array dependiendo del tipo del identificador
def getTipo(value):
    if isinstance(value, ArrayInfo):
        return value.tipo
    else:
        return value

#Dado un objeto correspondiente a un identificador almacenado en la tabla de símbolos retorna el tipo del identificador.
#En el caso de ser el objeto una instancia de ArrayInfo, simplemente retorna como tipo "array[m.. n]", donde m y n son los
#índices que limitan el arreglo y my n son constantes enteras tal que m <= n
#Parámetro:
#value: Objeto de la tabla de símbolos. Puede ser str o ArrayInfo
#retorna: int, bool, o array[m..n] dependiendo del tipo del identificador. m y n son constantes enteras con m <= n
def getTipoCompleto(value):
    if isinstance(value, ArrayInfo):
        return value.completeInfo()
    else:
        return value

#Permite almacenar información imortante de los arrays en la tabla de símbolos, como sus índice mínimo, índice máximo
#y longitud
class ArrayInfo:
    
    #Constructor de clase. info es un str de la forma m..n] con m y n literales enteros
    def __init__(self, info):
        self.tipo = "array"
        self.li = int(info.split("..")[0])
        self.ls = int(info.split("..")[1].split("]")[0])
        self.length = self.ls - self.li + 1

    #Verifica que el primer índice del arreglo sea menor o igual al último.
    #Retorna: True o False dependiendo de si se cumple o no la condición respectivamente
    def checkLimits(self):
        return self.li <= self.ls

    #Retorna: Un string de la forma array[m..n] donde m y n son el primer y último índice del arreglo
    #de acuerdo a la declaración del mismo
    def completeInfo(self):
        return self.tipo + "[" + str(self.li) + ".." + str(self.ls) + "]"

    #Retorna: la longitud del arrelo
    def getLength(self):
        return self.length


#Esta clase es la que representa la tabla de símbolos de GuardedUSB. Su único atributo es un diccionario, sin embargo se
#envolvió el mismo dentro de una clase para agruparlo con una serie de métodos que permiten la construcción de la tabla sin
#errores , así como otras funciones que son útiles a lo largo de la verificación de errores estáticos
class Symbol_Table:
    def __init__(self):
        self.table ={}

    #Llena la información de la tabla de símbolos. Verifica que ninguna variable se declare dos veces o que los arreglos
    #no tengan primer índice mayor al último
    #Parámmetro: 
    # varList: Es una lista de tuplas donde la primera coordenada es el identificador y la segunda el tipo. La lista
    #corresponde a todas las variables del bloque
    #SI detecta un error en la construcción de la tabla (Como los mencionados anteriormente) aborta la ejecución y notifica
    #al usuario
    def fillTable(self, varList):
        if varList is not None:
            for i in range(len(varList)):
                if self.table.get(varList[i][0]) is None:
                    if varList[i][1] == "int" or varList[i][1] == "bool":
                        self.table[varList[i][0]] = varList[i][1]
                    else:
                        self.table[varList[i][0]] = ArrayInfo(varList[i][1].split("[")[1])
                        if not self.table[varList[i][0]].checkLimits():
                            print("Error: El arreglo " + varList[i][0] + " tiene el límite inferior superior al inferior")
                            sys.exit()
                else:
                    print("Error: La variable " + varList[i][0] + " ha sido declarada dos veces en el mismo bloque")
                    sys.exit()

    ## Llena una tabla que solo contiene la variable de control del ciclo for
    # parámetro:
    # var: Variable de control del ciclo for 
    def fillTableFor(self, var):
        if var is not None:
            self.table[var] = var

    # Imprime la tabla de símbolos
    # Parámetro: 
    # indent: nivel de indentación del bloque al que pertenece la tabla
    def printSymbolTable(self, indent):
        print(indent + "Symbol table")
        infoIndent = indent + " "
        iterator = iter(self.table)
        for key in iterator:
            value = self.table[key]
            if isinstance(value, ArrayInfo):
                tipoCompleto = value.completeInfo()
                print(infoIndent + "variable: " + key + " | type: " +  tipoCompleto)
            else:
                print(infoIndent + "variable: " + key + " | type: " +  value)

    #Dado un identificador, busca en la tabla de símbolos el objeto que representa en la tabla al tipo de dicho identificador
    #Parámetro
    # key: Nombre del identificador
    # Retorna: El objeto asociado al identificador si este está en la tabla, None si no
    def getValue(self, key):
        try:
            return self.table[key]
        except:
            return None

    #Retorna el diccionario asociado a la tabla de símbolos
    def getTable(self):
        return self.table

#Esta clase es la de los nodos que forman el AST. Cada nodo de esta clase (o que hereda de esta clase) tiene 
#una categoría (Exp, AritOp, ident, etc.) dependiendo del objeto que representa dentro del lenguaje, un valor
#que es lo que se imprime en el árbol y una lista de hijps
class Node:
    #Constructor de clase Node
    #Parámetros:
    # category: categoría del nodo
    # value: Valr que debe imprimir el nodo
    # children: Lista con los nodos hijos. Si no se le pasa este parámtro, por default se le asigna la lista vacía
    def __init__(self, category, value, children=None):
        self.category = category
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []

    #Imprime el AST en el formato solicitado en el enunciado del proyecto
    #Parámetro:
    # ident: Nivel de indentación que debe tener la informacióna a imprimir dependiendo de la profundidad
    # del nodo en el árbol
    def printTree(self, indent):

        if (self.category == "Ident" or self.category == "Literal"):
            print(indent + self.category + ": " + str(self.value))
        elif isinstance(self, BlockNode):
            print(indent + self.value)
            self.symbol_table.printSymbolTable(indent + " ")
        else:
            print(indent + self.value)

        for i in range(len(self.children)):
            self.children[i].printTree(indent + " ")

    #Dada una pila que contiene todas las tablas de símbolos que están dentro del alcance de una instrucción
    #(ordenadas de la tabla del bloque más interno al más externo) busca ordenadamente si el identificador 
    #asociado al nodo está en alguna de ellas
    #Parámetro:
    # symbolTableStack: Pila de tablas de símbolos alcanzables
    #Retorna:
    # El objeto asociado al identificador dentro de la tabla más interna en la que se encuentre dicho identificador
    # si el identificador está en una tabla. None si no
    def searchTables(self, symbolTableStack):
        value = None
        for i in range(len(symbolTableStack)):
            value = symbolTableStack[i].getValue(self.value)
            if value is not None:
                return value
        return value

    #Dada la pila que almacena las variables de control de ciclos for sin cerrar, verifica que el identificador asocaido 
    # al nodo self no sea una de estas variable de control.
    #Retorna: True si el identificador no se corresponde a ninguna variable de control, false en caso contrario
    def searchForTables(self, symbolForTableStack):
        for i in range(len(symbolForTableStack)):
            value = symbolForTableStack[i].getValue(self.value)
            if value is not None:
                return False
        return True

    #Verifica si un identificador es de un tipo determinado
    # Parámetros:
    # tipo: Tipo del cual se espera sea la variable
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # cont le indica a la función que debe continuar su proceso y no terminar la ejecución si encuentra algo inesperado
    #esto permite que el semantic analyzer no colapse cuando está verificando si == o != son de tipo booleano o aritmético
    # Retorna; True si el identificador corresponde a una variable de tipo determinado
    #Si el identificador no se corresponde y cont=None, si la variable no fue declarada o si es de control de un for
    #genera un error y acaba la ejecución del programa
    def checkIdent(self, tipo, stack, forStack, cont=None):
        if self.searchForTables(forStack):
            value = self.searchTables(stack)
            varTipo = getTipoCompleto(value)
            if varTipo == tipo:
                return True
            else:
                if varTipo:
                    if cont:
                        return False
                    print("Error: La variable " + self.value + " es de tipo " + varTipo\
                        + " pero debe ser de tipo " + tipo)
                    sys.exit()
                else:
                    print("Error: Variable " + self.value + " no declarada")
                    sys.exit()
        else:
            print("Error: Se está cambiando el valor de una variable iterable del for: " + self.children[0].value)
            sys.exit()

    #Esta función es utilizada únicamente utilizada para ver si un identificador es de tipo array, sin importar índices
    #o longitud del arreglo
     # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # Retorna; True si el identificador corresponde a una variable de tipo determinado
    #Si el identificador no se corresponde con el tipo y cont=None, si la variable no fue declarada o si es de control 
    # de un for genera un error y acaba la ejecución del programa
    def checkArrayIdent(self, stack, forStack):
        if self.searchForTables(forStack):
            value = self.searchTables(stack)
            varTipo = getTipo(value)
            if varTipo == "array":
                return True
            else:
                if varTipo:
                    print("La variable " + self.value + " es de tipo " + varTipo + " pero debe ser de tipo array")
                    sys.exit()
                else:
                    print("Error: Variable " + self.value + " no declarada")
                    sys.exit()
        else:
            print("Se está cambiando el valor de una variable iterable del for: " + self.children[0].value)
            sys.exit()


    #Dado un arreglo cuyo identificador ya sabemos es de tipo array, verifica si el arreglo incluye asignaciones. 
    # Si las incluye, llama a checkArrayAsig
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    #Retorna:
    # True si no hay asignaciones o si las asignaciones ncluyen expresiones semánticamente correctas
    # Si alguna de las asignaciones no es semánticamente correcta, la función que descubra el error se encargará
    # de dar un mensaje de error y abortar la ejecución
    def checkArray(self, stack, forStack):
        if len(self.children) == 1:
            return True
        else:
            return self.checkArrayAsig(stack, forStack)          

    #Verifica si las expresiones dentro de la asignación de arreglos son válidas desde un punto de vistas emántico
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # Retorna: True si las expresioones dentro de la asignación son correctas
    # Si alguna de las asignaciones no es semánticamente correcta, la función que descubra el error se encargará
    # de dar un mensaje de error y abortar la ejecución
    def checkArrayAsig(self, stack, forStack):
        return self.children[1].checkArithmeticExp(stack, forStack) and self.children[2].checkArithmeticExp(stack, forStack)

    #Verifica si la operación de consulta de arreglos es semánticamente válida
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # Retorna: True si las expresiones dentro de la consulta son semánticamente correctas y si la consulta se aplica sobre
    # un identificador que represente a un array
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayConsult(self, stack, forStack):
        if self.children[0].category == "Ident":
            if self.children[0].checkArrayIdent(stack, forStack):
                    return self.children[1].checkArithmeticExp(stack, forStack)
        elif self.children[0].category == "ArrayOp" and self.children[0].value == "ArrayAsig":
            if self.children[0].checkArrayAsig(stack, forStack):
                return self.children[0].checkArrayConsult(stack, forStack)
        else:
            print("Error: Se está aplicando la operación consulta a algo que no es un arreglo")
            sys.exit()

    #Verifica que la longitud de los elementos utilizados para inicializar un arreglo coincidan con la longitud
    #del arreglo según su declaración
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # varName; Nombre de la variable qque se desea inicializar
    # Retorna: True si las expresioones dentro de la asignación son correctas
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayLength(self, stack, forStack, varName):
        if self.children[0].checkArithmeticExp(stack, forStack):
            if len(self.children) > 1:
                initLength = self.children[1].checkArrayInit(stack, forStack, varName) + 1
            else:
                initLength = 1

            #Busco la longitud del arreglo en las tablas de símbolos
            for i in range(len(stack)):
                varLength = stack[i].getValue(varName).getLength()
                if varLength:
                    break

            if initLength == varLength:
                return True
            else:
                print("Error: El arreglo " + varName + " fue inicializado con un número de elementos distintos al declarado")
                sys.exit()
        else:
            print("Error: Expresión no aritmética en la inicialización del arreglo " + varName)
            sys.exit()

    #Función auxiliar de checkArrayLength (arriba) que le permite llevar la cuenta de la longitud de la lista
    #que se utiliza para inicializar el arreglo
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # varName; Nombre de la variable qque se desea inicializar
    # Retorna: Número de elementos en la ista contando desde el final hasta el elemento sobre el que se llama la función
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayInit(self, stack, forStack, varName):
        if self.value == "ArrElementInit":
            if self.children[0].checkArithmeticExp(stack, forStack):
                if len(self.children) > 1:
                    return self.children[1].checkArrayInit(stack, forStack, varName) + 1
                else:
                    return 1
            else:
                print("Error: Expresión no aritmética en la inicialización del arreglo " + varName)
                sys.exit()
        else:
            if self.checkArithmeticExp(stack, forStack):
                return 1

    #Función ue verifica (en una asignación con arreglos) que el arreglo del lado izquierdo de la asignación sea del mismo
    #tipo que el arreglo de lado derecho delaasignación. También verifica que si hay una asignación de un elemento dentro del 
    # array del lado izquierdo las expresiones dentro de la asignación sean semánticamente válidas
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # varName; Nombre de la variable qque se desea inicializar
    # Retorna: True si las variables del lado izquierdo y derecho corresponden al mismo tipo de arreglo y si las
    #expresiones dentro de las asignaciones al arreglo del lado derecho son semánticamente correctas
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayType(self, stack, forStack, varName):
        if self.checkArrayAsig(stack, forStack):
            for i in range(len(stack)):
                arrayType = stack[i].getValue(varName).completeInfo()
                if arrayType:
                    break
            return self.children[0].checkOriginalArray(stack, forStack, varName, arrayType)

    #Para la operación asignación de arreglos, verifica todas las expresiones dentro de las asignaciones y cuando consigue la
    #variable a la cual se le están aplicando las modificaciones, verifica que sea del mismo tipo de array que la 
    #variable del lado izquierdo de la asignación
    def checkOriginalArray(self, stack, forStack, varName, arrayType):
        if self.category == "ArrayOp" and self.value == "ArrayAsig":
            if self.checkArrayAsig(stack, forStack):
                return self.children[0].checkOriginalArray(stack, forStack, varName, arrayType)
        elif self.category == "Ident":
            return self.checkIdent(arrayType, stack, forStack)
        else:
            print("Error: Operando inesperado " + self.getValue() + ". Se esperaba asignación de arreglo o variable")
            sys.exit()


    #Verificación de que el parámetro que se le pasa a la función sea un arreglo que cumpla con las condiciones dadas
    #por la especificación del lenguaje
    def checkFunction(self, stack, forStack, function):
        if self.children[0].category == "Ident":
            var = self.children[0].searchTables(stack) #Verificamos que la variable esté en la tabla se símbolos
            if var is not None: #Si está 
                varTipo = getTipo(var)
                if varTipo == "array": #Verifico el tipo
                    if function == "atoi": #La función atoi requiere verificación adicional del tamaño del arreglo
                        if (var.getLength()) == 1: #si el tamaño es 1
                            return self.checkArray(stack, forStack)
                        else:
                            print("Error: El arreglo " + self.children[0].getValue() + " tiene más de un elemento la función atoi() no se puede invocar")
                            sys.exit()
                    else: #Las demás no rquieren verificación adicional
                        return self.checkArray(stack, forStack)
                else:
                    print("Error: La variable " + self.children[0].getValue() + " no representa un arreglo. La función\
                        utilizada no es aplicable")
                    sys.exit()
            else: #La variable no está en la tabla
                print("Error: Variable " + self.children[0].value + " no declarada")
                sys.exit()
        elif self.children[0].category == "ArrayOp" and self.children[0].value == "ArrayAsig": #si el arreglo estpa modificado
            if self.children[0].checkArrayAsig(stack, forStack):
                return self.children[0].checkFunction(stack, function)
        else:
            print("Error: El parámetro de la función no es del tipo soportado por la misma (array)")
            sys.exit()

    #Verifica el tipo de expresión se corresponda con el tipo de la variable 
    def checkAsig(self, stack, forStack):
        print("Hello there")
        if self.children[0].searchForTables(forStack): #Verificamos si la variable está dentro de la tabla de For
            tipo = self.children[0].searchTables(stack)
            if tipo is not None:
                if tipo == "int":
                    print("YEY")
                    if self.children[1].children[0].checkArithmeticExp(stack, forStack):
                        print("YA CASI")
                        self.children[1].setValue("ArithExp")
                        return True
                elif tipo == "bool":
                    if self.children[1].children[0].checkBoolExp(stack, forStack):
                        self.children[1].setValue("BoolExp")
                        return True
                else:
                    if self.children[1].children[0].checkArrayExp(stack, forStack, self.children[0].getValue()):
                        self.children[1].setValue("ArrayExp")
                        return True
            else:
                print("Error: Variable " + self.children[0].value + " no declarada")
                sys.exit()
        else:
            print("Error: Se está cambiando el valor de una variable iterable del for: " + self.children[0].value)
            sys.exit()

    #Verifica que una expresión sea de tipo bool
    #cont le indica a la función que debe continuar su proceso y no terminar la ejecución si encuentra algo inesperado
    #esto permite que el semantic analyzer no colapse cuando está verificando si == o != son de tipo booleano o aritmético
    def checkBoolExp(self, stack, forStack, cont=None):
        if self.category == "BinOp":
            if self.children[0].checkBoolExp(stack, forStack, True) and self.children[1].checkBoolExp(stack, forStack, True):
                self.value = "BoolEqual"
                return True
            elif self.children[0].checkArithmeticExp(stack, forStack, True) and self.children[1].checkArithmeticExp(stack, forStack, True):
                self.value = "ArithEqual"
                return True
            else:
                print("Error: El operador " + self.getValue() + " no está comparando expresiones del mismo tipo o está comparando arrays")
                sys.exit()
        elif self.category == "RelOp":
            return self.children[0].checkArithmeticExp(stack, forStack) and self.children[1].checkArithmeticExp(stack, forStack)
        elif self.category == "BoolOp" and self.value != "Not":
            return self.children[0].checkBoolExp(stack, forStack) and self.children[1].checkBoolExp(stack, forStack)
        elif self.category == "BoolOp" and self.value == "Not":
            return self.children[0].checkBoolExp(stack, forStack) or self.children[0].checkArithmeticExp(stack, forStack)
        elif self.category == "Ident":
            return self.checkIdent("bool", stack, forStack, cont)
        elif self.category == "Literal":
            if self.getValue() == "true" or self.value == "false":
                return True
            else:
                if cont:
                    return False
                print("Error: El literal " + self.getValue() + " no es de tipo bool")
                sys.exit()
        else:
            if cont:
                return False
            print("Error: El operador " + self.value + " no es válido en esta expresión")
            sys.exit()


    #Verifica que una expresión sea de tipo aritmética
    #cont le indica a la función que debe continuar su proceso y no terminar la ejecución si encuentra algo inesperado
    #esto permite que el semantic analyzer no colapse cuando está verificando si == o != son de tipo booleano o aritmético
    def checkArithmeticExp(self, stack, forStack, cont=None):
        if self.category == "AritOp":
            return self.children[0].checkArithmeticExp(stack, forStack) and self.children[1].checkArithmeticExp(stack, forStack)
        elif self.category == "UnaryMinus":
            return self.children[0].checkArithmeticExp(stack, forStack)
        elif self.category == "BinOp" and self.value == "Mod":
            return (self.children[0].checkArithmeticExp(stack, forStack) and self.children[1].checkArithmeticExp(stack, forStack))
        elif self.category == "Function":
            return self.checkFunction(stack, forStack, self.value)
        elif self.category == "ArrayOp" and self.value == "ArrConsult":
            return self.checkArrayConsult(stack, forStack)
        elif self.category == "Exp":
            if self.children[0].checkArithmeticExp(stack, forStack):
                self.value = "ArithExp"
                return True
        elif self.category == "Ident":
            return self.checkIdent("int", stack, forStack, cont)
        elif self.category == "Literal":
            if self.value != "true" and self.value != "false":
                return True
            else:
                if cont:
                    return False
                print("El literal " + self.getValue() + " no es de tipo int")
                sys.exit()
        else:
            if cont:
                return False
            print("El operador " + self.value + " no es válido en esta expresión")
            sys.exit()

    def checkArrayExp(self, stack, forStack, varName=None):
        if self.category == "ArrayOp":
            if self.value == "ArrayAsig":
                return self.checkArrayType(stack, forStack, varName)
            elif self.value == "ArrElementInit":
                return self.checkArrayLength(stack, forStack, varName)
            else:
                print("Error: Asignación de valor int a una variable de tipo array")
                sys.exit()
        else:
            if self.category == "Ident":
                for i in range(len(stack)):
                    arrayType = stack[i].getValue(varName).completeInfo()
                    if arrayType:
                        break
                return self.checkIdent(arrayType, stack, forStack)
            else:
                print("Error: Se está utilizando operador " + self.value + ", que no es para elementos de tipo array")

    def checkArrayExpInString(self, stack, forStack):
        if self.category == "ArrayOp" and self.getValue() == "ArrayAsig":
            if self.checkArrayAsig(stack, forStack):
                return self.children[0].checkArrayExpInString(stack, forStack)
        elif self.category == "Ident":
            return self.checkArrayIdent(stack, forStack)
        # else:
        #     print("Otro error en concat")
        #     self.category()
        #     sys.exit()

    def checkStringContent(self, stack, forStack):
        if self.category == "Exp":
            if self.children[0].checkArithmeticExp(stack, forStack, True):
                self.setValue("ArithExp")
                return True
            elif self.children[0].checkBoolExp(stack, forStack, True):
                self.setValue("BoolExp")
                return True
            elif self.children[0].checkArrayExpInString(stack, forStack):
                self.setValue("ArrayExp")
                return True
        else:
            return True

    def checkConcat(self, stack, forStack):
        if self.children[0].category == "Concat":
            if self.children[0].children[0].checkStringContent(stack, forStack):
                return self.children[0].children[1].checkConcat(stack, forStack)
        else:
            return self.children[0].checkStringContent(stack, forStack)

    def checkFor(self, stack, forStack):
        forStack.insert(0, self.children[0].children[0].symbol_table)  #Insertamos la nueva tabla de símbolos
        if self.children[1].checkStaticErrorsAux(stack, forStack): ## Chequeamos los errores estáticos del ProgramBlock que contiene el For
            forStack.pop(0) #Cuando termino de ejecutar el for desempilo la variable de control
            return True

    def checkGuards(self, stack, forStack):
        if self.children[0].children[0].checkBoolExp(stack, forStack): ## Si la expresión corresponde con un bool, entonces seguimos
            self.children[0].setValue("BoolExp")
            if (len(self.children) > 2):  ### y seguimos chequeando los StaticErrors de las instrucciones y guardias
                child1 = self.children[1].checkStaticErrorsAux(stack, forStack) ## Chequeamos errores staticos de las instrucciones
                child2 = self.children[2].checkStaticErrorsAux(stack, forStack) ## Ahora para las demás guardias
                return child1 and child2
            else: 
                return self.children[1].checkStaticErrorsAux(stack, forStack) ## No hay más guardias, así que solo chequeamos las instrucciones
        else:
            print("Error: La expresión " + self.children[0].value + " no es de tipo bool para una guardia del If")
            sys.exit()



    #Inicial el procedimiento de análisis semántico del AST
    def checkStaticErrors(self):
        tableStack = []
        forTableStack = []
        return self.checkStaticErrorsAux(tableStack, forTableStack)

    #Esta función verifica los distintos tipos de nodos que tiene el árbol y verifica que todo tenga sentido desde el
    #punto de vista semántico
    def checkStaticErrorsAux(self, stack, forStack):
        if isinstance(self, BlockNode):
            return self.checkBlock(stack, forStack)
        elif self.category == "For":
            return self.checkFor(stack, forStack)
        elif self.category == "Asig":
            return self.checkAsig(stack, forStack)
        ## Chequeamos que el body y la lista de guardias del if la expresión sea booleana
        elif self.category == "Body" or self.category == "Guard":
            return self.checkGuards(stack, forStack)
        elif self.category == "InstSequence":
            if len(self.children) == 2:
                return all([self.children[0].checkStaticErrorsAux(stack, forStack), self.children[1].checkStaticErrorsAux(stack, forStack)])
            else:
                return self.children[0].checkStaticErrorsAux(stack, forStack)
        elif self.category == "if" or self.category == "do":
            return self.children[0].checkStaticErrorsAux(stack, forStack)
        elif self.category == "Read":
            return all([self.children[0].searchForTables(forStack), self.searchTables(stack) is not None])
        elif self.category == "print" or self.category == "println":
            if len(self.children) == 1:
                self.children[0].checkStringContent(stack, forStack)
            else:
                if self.children[0].checkStringContent(stack, forStack):
                    return self.children[1].checkStaticErrorsAux(stack, forStack)
        elif self.category == "Concat":
            return self.checkConcat(stack, forStack)
        else:
            print("Error inesperado")
            print(self.category)
            sys.exit()

    def getValue(self):
        return self.value

    def setValue(self, newValue):
        self.value = newValue

class DecNode(Node):
    def __init__(self, category, value, tupleList, children=None, last=None):
        super().__init__(category, value, children)
        self.declaredVars = tupleList
        self.lastLine = last

    def getDeclaredVars(self):
        return self.declaredVars

    #Esto me permite que cada línea de declaración se vea como hija de la línea anterior
    def addChildren(self, newChildren):
        if self.lastLine: #Si esta es la última línea de declaración leída, el hijo va aquí
            sequence = len(self.children) #Esta es la ubicación en la lista de hijos donde va el nuevo hijo
            self.lastLine = False #Esta ya no es la última línea declarada
            self.children = self.children + newChildren
            self.children[sequence].children[0].lastLine = True
        else: #Si no, debemos revisar la siguiente línea
            sequence = len(self.children) - 1 #Ubicación en la lista de hijos donde va el nodo secuenciación
            self.children[sequence].children[0].addChildren(newChildren)

    #Une la lista de tuplas de una línea de declaración con la de la línea siguiente, de manera que el block pueda
    #usar esta lista para crear la tabla de símbolos correspondiente a todas las declaraciones
    def addTupleList(self, newTuples):
        self.declaredVars += newTuples

class ForNode(Node):
    
    def __init__(self, category, value, children=None, var=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table()
        self.symbol_table.fillTableFor(var)

class BlockNode(Node):
    
    def __init__(self, category, value, children=None, varList=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table()
        self.symbol_table.fillTable(varList)

    def checkBlock(self, stack, forStack):
        if bool(self.symbol_table.getTable()): #Si el bloque tiene variables declaradas
            stack.insert(0, self.symbol_table)  #Insertamos la nueva tabla de símbolos
            if (len(self.children) == 2): #Si hay solo una instrucción
                return self.children[1].checkStaticErrorsAux(stack, forStack)
            else:
                stackLength = len(stack) #Si hay una secuencia de instrucciones debemos guardar el tamaño del
                                            #stack ya que este puede variar dentro de la siguiente instrucción
                child1 = self.children[1].checkStaticErrorsAux(stack, forStack)
                while len(stack) != stackLength: #Si el stack varió lo devolvemos al estado en que estaba originalmente
                    stack.pop(0)
                child2 = self.children[2].checkStaticErrorsAux(stack, forStack)

                return child1 and child2
        else:
            return self.children[0].checkStaticErrorsAux(stack, forStack)
        

