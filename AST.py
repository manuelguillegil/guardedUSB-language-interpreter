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
        return value[0]

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
        return value[0]

def getBoolean(value):
    if value == "true":
        return True
    else:
        return False

########## Borrar esta función si al final no se utiliza ####################
def searchByName(varName, stack):
    for i in range(len(stack)):
        varType = stack[i].getValue(varName)
        if varType is not None:
            return varType
    
    print("Error inesperado en searchByName")
    sys.exit()


#Permite almacenar información imortante de los arrays en la tabla de símbolos, como sus índice mínimo, índice máximo
#y longitud
class ArrayInfo:
    
    #Constructor de clase. info es un str de la forma m..n] con m y n literales enteros
    def __init__(self, info):
        if type(info) is str:
            self.tipo = "array"
            self.li = int(info.split("..")[0])
            self.ls = int(info.split("..")[1].split("]")[0])
            self.length = self.ls - self.li + 1
            self.value = [None for i in range(self.ls - self.li + 1)]
        elif isinstance(info, ArrayInfo):
            self.tipo = "array"
            self.li = info.getMin()
            self.ls = info.getMax()
            self.length = info.getLength()
            self.value = [i for i in info.value]
        else:
            print("Error en la creación de estructura array")

    #Verifica que el primer índice del arreglo sea menor o igual al último.
    #Retorna: True o False dependiendo de si se cumple o no la condición respectivamente
    def checkLimits(self):
        return self.li <= self.ls

    def checkIndex(self, index):
        return self.li <= index <= self.ls

    #Retorna: Un string de la forma array[m..n] donde m y n son el primer y último índice del arreglo
    #de acuerdo a la declaración del mismo
    def completeInfo(self):
        return self.tipo + "[" + str(self.li) + ".." + str(self.ls) + "]"

    #Retorna: la longitud del arrelo
    def getLength(self):
        return self.length

    def getMax(self):
        return self.ls

    def getMin(self):
        return self.li

    def getArrayItems(self):
        return self.value

    def __getitem__(self, index):
        return self.value[abs(self.li - index)]

    def __setitem__(self, index, value):
        realIndex = abs(self.li - index)
        self.value[realIndex] = value

    def copyArray(self, newArray):
        for i in range(self.length):
            self.value[i] = newArray[i]

#Esta clase es la que representa la tabla de símbolos de GuardedUSB. Contiene el diccionario donde se almacenan los símbolos
#de la tabla y posee un atributo que indica si la tabla usada es la que almacena la variable de control de un ciclo for
class Symbol_Table:
    def __init__(self, isFor):
        self.table ={}
        self.isFor = isFor

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
                        self.table[varList[i][0]] = (varList[i][1], None)
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
            self.table[var] = (var, None)

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
            else:
                tipoCompleto = getTipo(value)
            print(infoIndent + "variable: " + key + " | type: " +  tipoCompleto)

    #Dado un identificador, busca en la tabla de símbolos el objeto que representa en la tabla al tipo de dicho identificador
    # Parámetro:
    # key: Nombre del identificador
    # Retorna: El objeto asociado al identificador si este está en la tabla, None si no
    def getValue(self, key):
        try:
            return self.table[key]
        except:
            return None

    def setValue(self, key, value):
        self.table[key] = value

    #Retorna el diccionario asociado a la tabla de símbolos
    def getTable(self):
        return self.table

#Esta clase es la de los nodos que forman el AST. Cada nodo de esta clase (o que hereda de esta clase) tiene 
#una categoría (Exp, AritOp, ident, etc.) dependiendo del objeto que representa dentro del lenguaje, un valor
#que es lo que se imprime en el árbol y una lista de hijos
class Node:
    #Constructor de clase Node
    #Parámetros:
    # category: categoría del nodo
    # value: Valr que debe imprimir el nodo
    # children: Lista con los nodos hijos. Si no se le pasa este parámetro, por default se le asigna la lista vacía.
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

    ############################################################################################################

    ################################ FUNCIONES DEL SEMANTIC ANALYZER ###########################################

    ############################################################################################################

    #Dada una pila que contiene todas las tablas de símbolos que están dentro del alcance de una instrucción
    #(ordenadas de la tabla del bloque más interno al más externo) busca ordenadamente si el identificador 
    #asociado al nodo está en alguna de ellas
    #Parámetro:
    # symbolTableStack: Pila de tablas de símbolos alcanzables
    #Retorna:
    # El objeto asociado al identificador dentro de la tabla más interna en la que se encuentre dicho identificador
    # si el identificador está en una tabla. None si no
    def searchTables(self, symbolTableStack):
        varType = None
        for i in range(len(symbolTableStack)):
            varType = symbolTableStack[i].getValue(self.value)
            if varType is not None:
                if symbolTableStack[i].isFor:
                    print("Error: Se está intentando manipular una variable de control de ciclo for")
                    sys.exit()
                return varType
        return varType

    #Verifica si un identificador es de un tipo determinado
    # Parámetros:
    # tipo: Tipo del cual se espera sea la variable
    # stack: Pila de tablas de símbolos
    # cont le indica a la función que debe continuar su proceso y no terminar la ejecución si encuentra algo inesperado
    #esto permite que el semantic analyzer no colapse cuando está verificando si == o != son de tipo booleano o aritmético
    # Retorna; True si el identificador corresponde a una variable de tipo determinado
    #Si el identificador no se corresponde y cont=None, si la variable no fue declarada o si es de control de un for
    #genera un error y acaba la ejecución del programa
    def checkIdent(self, tipo, stack, cont=None):
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

    # Esta función es utilizada únicamente para ver si un identificador es de tipo array, sin importar índices
    #o longitud del arreglo
     # Parámetros:
    # stack: Pila de tablas de símbolos
    # Retorna; True si el identificador corresponde a una variable de tipo determinado
    #Si el identificador no se corresponde con el tipo y cont=None, si la variable no fue declarada o si es de control 
    # de un for genera un error y acaba la ejecución del programa
    def checkArrayIdent(self, stack):
        value = self.searchTables(stack)
        varTipo = getTipo(value)
        if varTipo == "array":
            return True
        else:
            if varTipo:
                print("Error: La variable " + self.value + " es de tipo " + varTipo + " pero debe ser de tipo array")
                sys.exit()
            else:
                print("Error: Variable " + self.value + " no declarada")
                sys.exit()


    #Dado un arreglo cuyo identificador ya sabemos es de tipo array, verifica si el arreglo incluye asignaciones. 
    # Si las incluye, llama a checkArrayAsig
    # Parámetros:
    # stack: Pila de tablas de símbolos
    #Retorna:
    # True si no hay asignaciones o si las asignaciones ncluyen expresiones semánticamente correctas
    # Si alguna de las asignaciones no es semánticamente correcta, la función que descubra el error se encargará
    # de dar un mensaje de error y abortar la ejecución
    def checkArray(self, stack):
        if len(self.children) == 1:
            return True
        else:
            return self.checkArrayAsig(stack)          

    #Verifica si las expresiones dentro de la asignación de arreglos son válidas desde un punto de vistas emántico
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # Retorna: True si las expresioones dentro de la asignación son correctas
    # Si alguna de las asignaciones no es semánticamente correcta, la función que descubra el error se encargará
    # de dar un mensaje de error y abortar la ejecución
    def checkArrayAsig(self, stack):
        return self.children[1].checkArithmeticExp(stack) and self.children[2].checkArithmeticExp(stack)

    #Verifica que la longitud de los elementos utilizados para inicializar un arreglo coincidan con la longitud
    #del arreglo según su declaración
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # varName; Nombre de la variable qque se desea inicializar
    # Retorna: True si las expresioones dentro de la asignación son correctas
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayLength(self, stack, varName):
        if self.children[0].checkArithmeticExp(stack):
            if len(self.children) > 1:
                initLength = self.children[1].checkArrayInit(stack, varName) + 1
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
    # varName; Nombre de la variable qque se desea inicializar
    # Retorna: Número de elementos en la ista contando desde el final hasta el elemento sobre el que se llama la función
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayInit(self, stack, varName):
        if self.value == "ArrElementInit":
            if self.children[0].checkArithmeticExp(stack):
                if len(self.children) > 1:
                    return self.children[1].checkArrayInit(stack, varName) + 1
                else:
                    return 1
            else:
                print("Error: Expresión no aritmética en la inicialización del arreglo " + varName)
                sys.exit()
        else:
            if self.checkArithmeticExp(stack):
                return 1

    #Función ue verifica (en una asignación con arreglos) que el arreglo del lado izquierdo de la asignación sea del mismo
    #tipo que el arreglo de lado derecho delaasignación. También verifica que si hay una asignación de un elemento dentro del 
    # array del lado izquierdo las expresiones dentro de la asignación sean semánticamente válidas
    # Parámetros:
    # stack: Pila de tablas de símbolos
    # varName; Nombre de la variable qque se desea inicializar
    # Retorna: True si las variables del lado izquierdo y derecho corresponden al mismo tipo de arreglo y si las
    #expresiones dentro de las asignaciones al arreglo del lado derecho son semánticamente correctas
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkArrayType(self, stack, varName):
        if self.checkArrayAsig(stack):
            for i in range(len(stack)):
                arrayType = stack[i].getValue(varName).completeInfo()
                if arrayType:
                    break
            return self.children[0].checkOriginalArray(stack, varName, arrayType)

    #Función recursiva auxiliar de chekArrayType (arriba) que cumple el mismo propósito
     # Parámetros:
    # stack: Pila de tablas de símbolos
    # stack: Pila de variables de control de ciclo for
    # varName; Nombre de la variable qque se desea inicializar
    # arrayType: Tipo de arreglo al que pertenece la variable del lado izquierdo de la asignación
    # Retorna: True si las variables del lado izquierdo y derecho corresponden al mismo tipo de arreglo y si las
    #expresiones dentro de las asignaciones al arreglo del lado derecho son semánticamente correctas
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkOriginalArray(self, stack, varName, arrayType):
        if self.category == "ArrayOp" and self.value == "ArrayAsig":
            if self.checkArrayAsig(stack):
                return self.children[0].checkOriginalArray(stack, varName, arrayType)
        elif self.category == "Ident":
            return self.checkIdent(arrayType, stack)
        else:
            print("Error: Operando inesperado " + self.getValue() + ". Se esperaba asignación de arreglo o variable")
            sys.exit()


    #Verificación de que el parámetro que se le pasa a la función sea un arreglo que cumpla con las condiciones dadas
    #por la especificación del lenguaje
    # stack: Pila de tablas de símbolos
    # function: Nombre de la función aplicada sobre el arreglo
    # Retorna: True si el arreglo cumple con todas las especificaciones requiere el enunciado y si cualquier asignación
    #que se haga sobre el arreglo parámetro de la función es semánticamente correcta
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkFunction(self, stack, function):
        if self.children[0].category == "Ident":
            var = self.children[0].searchTables(stack) #Verificamos que la variable esté en la tabla se símbolos
            if var is not None: #Si está 
                varTipo = getTipo(var)
                if varTipo == "array": #Verifico el tipo
                    if function == "atoi": #La función atoi requiere verificación adicional del tamaño del arreglo
                        if (var.getLength()) == 1: #si el tamaño es 1
                            return self.checkArray(stack)
                        else:
                            print("Error: El arreglo " + self.children[0].getValue() + " tiene más de un elemento la función atoi() no se puede invocar")
                            sys.exit()
                    else: #Las demás no rquieren verificación adicional
                        return self.checkArray(stack)
                else:
                    print("Error: La variable " + self.children[0].getValue() + " no representa un arreglo. La función\
                        utilizada no es aplicable")
                    sys.exit()
            else: #La variable no está en la tabla
                print("Error: Variable " + self.children[0].value + " no declarada")
                sys.exit()
        elif self.children[0].category == "ArrayOp" and self.children[0].value == "ArrayAsig": #si el arreglo estpa modificado
            if self.children[0].checkArrayAsig(stack):
                return self.children[0].checkFunction(stack, function)
        else:
            print("Error: El parámetro de la función no es del tipo soportado por la misma (array)")
            sys.exit()

    #Verifica el tipo de expresión al lado derecho de la asginación se corresponda con el tipo de la variable
    # al lado izquierdo de la asignación 
    # stack: Pila de tablas de símbolos
    # Retorna: True si la expresión del lado derecho es una espresión ue se corresponde al tipo de la variable del lado
    # izquierdo y es una expresión semánticamente correcta
    # Si esta función o alguna de las funciones que llama detecta un error semántico muestra un mensaje de error y aborta
    #la ejecución del programa
    def checkAsig(self, stack):
        tipo = self.children[0].searchTables(stack)
        if tipo is not None:
            if getTipo(tipo) == "int":
                if self.children[1].children[0].checkArithmeticExp(stack):
                    self.children[1].setValue("ArithExp")
                    return True
            elif getTipo(tipo) == "bool":
                if self.children[1].children[0].checkBoolExp(stack):
                    self.children[1].setValue("BoolExp")
                    return True
            else:
                #Este trozo de código permite la inicialización de arreglos de longitud 1
                if tipo.getLength() == 1:
                    if self.children[1].children[0].checkArithmeticExp(stack, True):
                        newNode = Node("ArrayOp", "ArrElementInit", self.children[1].children)
                        self.children[1].children = [newNode]
                        self.children[1].setValue("ArrayExp")
                        return True

                if self.children[1].children[0].checkArrayExp(stack, self.children[0].getValue()):
                    self.children[1].setValue("ArrayExp")
                    return True
        else:
            print("Error: Variable " + self.children[0].value + " no declarada")
            sys.exit()
        
    #Verifica que una expresión sea de tipo bool
    #cont le indica a la función que debe continuar su proceso y no terminar la ejecución si encuentra algo inesperado
    #esto permite que el semantic analyzer no colapse cuando está verificando si == o != son de tipo booleano o aritmético
    def checkBoolExp(self, stack, cont=None):
        if self.category == "BinOp":
            if self.children[0].checkBoolExp(stack, True) and self.children[1].checkBoolExp(stack, True):
                if self.getValue() == "Equals":
                    self.value = "BoolEqual"
                else:
                    self.value = "BoolNequal"
                return True
            elif self.children[0].checkArithmeticExp(stack, True) and self.children[1].checkArithmeticExp(stack, True):
                if self.getValue() == "Equals":
                    self.value = "ArithEqual"
                else:
                    self.value = "ArithNequal"
                return True
            else:
                print("Error: El operador " + self.getValue() + " no está comparando expresiones del mismo tipo o está comparando arrays")
                sys.exit()
        elif self.category == "RelOp":
            return self.children[0].checkArithmeticExp(stack) and self.children[1].checkArithmeticExp(stack)
        elif self.category == "BoolOp" and self.value != "Not":
            return self.children[0].checkBoolExp(stack) and self.children[1].checkBoolExp(stack)
        elif self.category == "BoolOp" and self.value == "Not":
            return self.children[0].checkBoolExp(stack) or self.children[0].checkArithmeticExp(stack)
        elif self.category == "Ident":
            return self.checkIdent("bool", stack, cont)
        elif self.category == "Literal":
            if self.getValue() == "true" or self.value == "false":
                return True
            else:
                if cont:
                    return False
                print("Error: El literal " + str(self.getValue()) + " no es de tipo bool")
                sys.exit()
        else:
            if cont:
                return False
            print("Error: El operador " + self.value + " no es válido en esta expresión")
            sys.exit()


    #Verifica que una expresión sea de tipo aritmética
    #cont le indica a la función que debe continuar su proceso y no terminar la ejecución si encuentra algo inesperado
    #esto permite que el semantic analyzer no colapse cuando está verificando si == o != son de tipo booleano o aritmético
    def checkArithmeticExp(self, stack, cont=None):
        if self.category == "AritOp":
            return self.children[0].checkArithmeticExp(stack) and self.children[1].checkArithmeticExp(stack)
        elif self.category == "UnaryMinus":
            return self.children[0].checkArithmeticExp(stack)
        elif self.category == "Function":
            return self.checkFunction(stack, self.value)
        elif self.category == "ArrayOp" and self.value == "ArrConsult":
            return self.children[0].checkArrayExpIndependent(stack) and self.children[1].checkArithmeticExp(stack)
        elif self.category == "Exp":
            if self.children[0].checkArithmeticExp(stack):
                self.value = "ArithExp"
                return True
        elif self.category == "Ident":
            return self.checkIdent("int", stack, cont)
        elif self.category == "Literal":
            if self.value != "true" and self.value != "false":
                return True
            else:
                if cont:
                    return False
                print("Error: El literal " + self.getValue() + " no es de tipo int")
                sys.exit()
        else:
            if cont:
                return False
            print("El operador " + self.value + " no es válido en esta expresión")
            sys.exit()

    ## Verifica que la expresión en relación al Array cumpla con las condiciones del tipo de dato
    ## como lo puede ser los operadores para los elementos de tipo array, consultas y asignaciones
    ## Paramétros;
    ## stack de la tabla de símbolos y varName que es el nombre de la variable
    def checkArrayExp(self, stack, varName=None):
        if self.category == "ArrayOp":
            if self.value == "ArrayAsig":
                return self.checkArrayType(stack, varName)
            elif self.value == "ArrElementInit":
                return self.checkArrayLength(stack, varName)
            else:
                print("Error: Asignación de valor int a una variable de tipo array")
                sys.exit()
        else:
            if self.category == "Ident":
                for i in range(len(stack)):
                    arrayType = stack[i].getValue(varName).completeInfo()
                    if arrayType:
                        break
                return self.checkIdent(arrayType, stack)
            else:
                print("Error: Se está utilizando operador " + self.value + ", que no es para elementos de tipo array")
                sys.exit()

    ## Verifica que para un Array, que si es de categoria de operación sobre array y su valor es una asignación a un array
    ## entonces hacemos un llamado recursivo (con sus verificaciones correspondientes) hasta llegar al identificador y chequearlo
    def checkArrayExpIndependent(self, stack):
        if self.category == "ArrayOp" and self.getValue() == "ArrayAsig":
            if self.checkArrayAsig(stack):
                return self.children[0].checkArrayExpIndependent(stack)
        elif self.category == "Ident":
            return self.checkArrayIdent(stack)

    ## Verificamos el contenido de un String. Si el contenido es una expresión, chequeamos que corresponda con alguna expresión 
    ## de tipo aritmético, bool o de array
    def checkStringContent(self, stack):
        if self.category == "Exp":
            if self.children[0].checkArithmeticExp(stack, True):
                self.setValue("ArithExp")
                return True
            elif self.children[0].checkBoolExp(stack, True):
                self.setValue("BoolExp")
                return True
            elif self.children[0].checkArrayExpIndependent(stack):
                self.setValue("ArrayExp")
                return True
        else:
            return True

    ## Esta función nos permite verificar que cada string que se concatene podamos chequear su contenido que sea válido
    def checkConcat(self, stack):
        if self.children[0].category == "Concat":
            if self.children[0].children[0].checkStringContent(stack):
                return self.children[0].children[1].checkConcat(stack)
        else:
            return self.children[0].checkStringContent(stack)

    ## Permite añadir la tabla de símbolo del For y además luego de verificar las expresiones que la componen sea de tipo aritmético, 
    ## vamos a chequear los errores estáticos del hijo que corresponde al bloque de instrucciones del For
    ## Paramétros:
    ## Nodo de tipo ForNode y la pila de tablas de símbolo
    def checkFor(self, stack):
        stack.insert(0, self.children[0].children[0].symbol_table) 
        if self.children[0].children[0].children[0].checkArithmeticExp(stack) and self.children[0].children[0].children[1].checkArithmeticExp(stack):
            if self.children[1].checkStaticErrorsAux(stack):
                stack.pop(0)
                return True

    ## Verificamos para las guardias: Si la expresión corresponde con un bool, entonces seguimos y seguimos chequeando los StaticErrors de las instrucciones y los componentes de la guardia
    ## luego chequeamos errores staticos de las instrucciones para el primer hijo y si tiene un segundo hijo (que existen más guardias), chequeamos las demás guardias hasta llegar a la última
    def checkGuards(self, stack):
        if self.children[0].children[0].checkBoolExp(stack):
            self.children[0].setValue("BoolExp")
            if (len(self.children) > 2):  
                child1 = self.children[1].checkStaticErrorsAux(stack) 
                child2 = self.children[2].checkStaticErrorsAux(stack)
                return child1 and child2
            else: 
                return self.children[1].checkStaticErrorsAux(stack)
        else:
            print("Error: La expresión " + self.children[0].value + " no es de tipo bool para una guardia del If")
            sys.exit()

    #Inicial el procedimiento de análisis semántico del AST
    def checkStaticErrors(self):
        tableStack = []
        return self.checkStaticErrorsAux(tableStack)

    # Esta función verifica los distintos tipos de nodos que tiene el árbol y verifica que todo tenga sentido desde el
    # punto de vista semántico. Para ello consideramos las instancias de los BlockNode, categorias de tipo For, Asig, Body, InstSequence, If, Read, etc...
    ## también se incluye el caso de que exista un error inesperado con las categorías de cada Nodo que vayamos a chequear al no corresponder con alguna de estas categorías válidas
    ## y por lo tanto imprime la categoría error y aborta
    def checkStaticErrorsAux(self, stack):
        if isinstance(self, BlockNode):
            return self.checkBlock(stack)
        elif self.category == "For":
            return self.checkFor(stack)
        elif self.category == "Asig":
            return self.checkAsig(stack)
        elif self.category == "Body" or self.category == "Guard":
            return self.checkGuards(stack)
        elif self.category == "InstSequence":
            if len(self.children) == 2:
                return all([self.children[0].checkStaticErrorsAux(stack), self.children[1].checkStaticErrorsAux(stack)])
            else:
                return self.children[0].checkStaticErrorsAux(stack)
        elif self.category == "if" or self.category == "do":
            return self.children[0].checkStaticErrorsAux(stack)
        elif self.category == "Read":
            return self.children[0].searchTables(stack) is not None
        elif self.category == "print" or self.category == "println":
            if len(self.children) == 1:
                self.children[0].checkStringContent(stack)
            else:
                if self.children[0].checkStringContent(stack):
                    return self.children[1].checkStaticErrorsAux(stack)
        elif self.category == "Concat":
            return self.checkConcat(stack)
        else:
            print("Error inesperado")
            print(self.category)
            sys.exit()

    ############################################################################################################
    
    ################################################## EVALUADOR ###############################################
    
    ############################################################################################################

    #Dada una variable, guarda su valor en la tabla
    def setVarValue(self, symbolTableStack, newValue):
        varType = None
        for i in range(len(symbolTableStack)):
            varType = symbolTableStack[i].getValue(self.value)
            if varType is not None:
                symbolTableStack[i].setValue(self.value, (varType[0], newValue))
            else:
                print("Error en ejecución: setVarValue")
                sys.exit()

    def setArrayValue(self, symbolTableStack, newValue):
        varType = None
        for i in range(len(symbolTableStack)):
            varType = symbolTableStack[i].getValue(self.value)
            if varType is not None:
                varType.copyArray(newValue)
                symbolTableStack[i].setValue(self.value, varType)
            else:
                print("Error en ejecución: setArrayValue")
                sys.exit()

    #Retorna el valor de una variable. Si no ha sido inicializada, devuelve error
    def checkInitIdent(self, stack):
        idValue = self.searchTables(stack)
        if idValue[0] == "int" or idValue[0] == "bool":
            if idValue[1] is not None:
                return idValue[1]
            else:
                print("Error: Variable " + self.value + " no inicializada")
                sys.exit()
        else: #arrays
            if idValue[idValue.getMin()] is not None:
                return idValue.getArrayItems()
            else:
                print("Error: Variable " + self.value + " no inicializada")
                sys.exit()
    
    #Esta función se utiliza para verificar sobre qué arreglo debemos llamar la función embebida y 
    #si tiene asignaciones, que ninguna se haga fuera del rango del arreglo
    def findArray(self, stack):
        if self.children[0].category == "Ident":
            array = self.children[0].searchTables(stack)
            if array[array.getMin()] == None:
                print("Error: El arreglo " + self.getValue() + " no ha sido inicializado")
                sys.exit()
        else:
            array = self.children[0].findArray(stack)
        
        if len(self.children) == 3:
            index = self.children[1].evalArithmeticExp(stack)

            if array.checkIndex(index):
                return array
            else:
                print("Error de ejecución: Índice fuera de rango")
                sys.exit()
        else:
            return array

    #si se hace consulta sobre un arreglo, se calcula el arreglo que fue consultado, en caso de que incluya
    #asignaciones. Si no incluye asignaciones, solo retona el valor almacenado del arreglo. Si el arreglo no incluye asignaciones
    #devuelve el valor del arreglo
    def arrayValue(self, stack):
        if self.children[0].category == "Ident":
            array = self.children[0].searchTables(stack)
            copy = ArrayInfo(array)
            if copy[copy.getMin()] is None: ##Si el arreglo original no ha sido inicializado es un error
                print("Error: El arreglo " + self.getValue() + " no ha sido inicializado")
                sys.exit()
        else:
            copy = self.children[0].arrayValue(stack)

        index = self.children[1].evalArithmeticExp(stack)

        if len(self.children) == 3:
            if copy.checkIndex(index):
                value = self.children[2].evalArithmeticExp(stack)
                copy[index] = value
                return copy
            else:
                print("Error: Índice " + str(index) + " fuera del rango del arreglo")
                sys.exit()
        else:
            return copy

    def InitializeArray(self, stack, newArray):
        element = self.children[0].evalArithmeticExp(stack)
        newArray.append(element)
        if len(self.children) > 1:
            if self.children[1].getValue() == "ArrElementInit":
                self.children[1].InitializeArray(stack, newArray)
            else:
                element = self.children[1].evalArithmeticExp(stack)
                newArray.append(element)

    def evalRead(self, stack):
        tipo = self.children[0].searchTables(stack)
        if isinstance(tipo, ArrayInfo):
            while True:
                try:
                    arrayItems = input("Introduzca arreglo de longitud " + str(tipo.getLength()) + ": ")
                    items = arrayItems.split(",")
                    newArray = [int(i) for i in items]
                    assert(len(newArray) == tipo.getLength())
                    break
                except:
                    print("Error. Pudo ser por: No utilizar el formato correcto, no utilizar literales numéricos o por cantidad incorrecta de elementos")
            self.children[0].setArrayValue(stack, newArray)
        else:
            while True:
                try:
                    item = input("Introduzca una variable de tipo " + tipo[0] + ": ")
                    if item == "true" or item == "false":
                        assert tipo[0] == "bool"
                        value = getBoolean(item)
                        break
                    else:
                        value = int(item)
                        break
                except:
                    print("Error: La información introducida no se corresponde al tipo de la variable")

            self.children[0].setVarValue(stack, value)

        return True

    def evalFor(self, stack, numIteraccion):
        iterator = numIteraccion
        start = self.children[0].children[0].children[0].evalArithmeticExp(stack)
        end = self.children[0].children[0].children[1].evalArithmeticExp(stack)
        totalNumIteration = end - start

        if (numIteraccion == totalNumIteration):
            return True
            #totalNumIteration = end - start

        ## Este es el Programblock
        self.children[1].evaluatorAux(stack)
        iterator = iterator + 1
        return self.evalFor(stack, iterator) ## Creamos otro ciclo del For

    def evalPrintAux(self, stack):
        self.buildPrint(self.evalPrint(stack) + self.children[1].evaluatorAux(stack))
        if(self.category == 'print'):
            self.print()
        else:
            self.println()
        return True

    def evalPrint(self, stack):
        return self.children[0].evalStringContent(stack)

    def evalStringContent(self, stack):
        if self.category == "Exp":
            if self.children[0].checkArithmeticExp(stack, True):
                return str(self.children[0].evalArithmeticExp(stack))
            elif self.children[0].checkBoolExp(stack, True):
                return str(self.children[0].evalBoolExp(stack))
            elif self.children[0].checkArrayExpIndependent(stack):
                return str(self.children[0].evalArrayExpForPrint(stack))
        else:
            return str(self.value)

    def checkInitIdentForPrint(self, stack):
        idValue = self.searchTables(stack)
        mi = idValue.getMin()
        ma = idValue.getMax()
        if idValue[idValue.getMin()] is not None:
            arrayInfo = idValue.getArrayItems()
            resultForPrint = ''
            i = mi
            while i < ma + 1:
                if(i != ma):
                    resultForPrint = resultForPrint + str(i) + ':' + str(arrayInfo[0]) + ', '
                else:
                    resultForPrint = resultForPrint + str(i) + ':' + str(arrayInfo[0])
                i += 1
            return resultForPrint
        else:
            print("Error: Variable " + self.value + " no inicializada")
            sys.exit()

    def evalConcat(self, stack):
        if self.children[0].category == "Concat":
            return self.children[0].children[0].evalStringContent(stack) + self.children[0].children[1].evalPrint(stack)
        else:
            return self.children[0].evalStringContent(stack)

    def evalConcat(self, stack):
        if self.children[0].category == "Concat":
            return self.children[0].children[0].evalStringContent(stack) + self.children[0].children[1].evalPrint(stack)
        else:
            return self.children[0].evalStringContent(stack)

    def evalAsig(self, stack):
        tipo = self.children[0].searchTables(stack)
        if getTipo(tipo) == "int":
            result = self.children[1].children[0].evalArithmeticExp(stack)
            # print(self.children[0].getValue())
            # print(result)
            self.children[0].setVarValue(stack, result)
            return True
        elif getTipo(tipo) == "bool":
            result = self.children[1].children[0].evalBoolExp(stack)
            self.children[0].setVarValue(stack, result)
            # print(self.children[0].getValue())
            # print(result)
            return True
        else:
            result = self.children[1].children[0].evalArrayExp(stack)
            self.children[0].setArrayValue(stack, result)
            # print(self.children[0].getValue())
            # print(result)
            return True

    def evalArithmeticExp(self, stack):
        if isinstance(self, BinOpNode):
            op1 = self.children[0].evalArithmeticExp(stack)
            op2 = self.children[1].evalArithmeticExp(stack)
            return self.efectuateOperation(op1, op2)
        elif isinstance(self, UnaryMinusNode):
            op1 = self.children[0].evalArithmeticExp(stack)
            return self.efectuateOperation(op1)
        elif isinstance(self, FunctionNode):
            op1 = self.findArray(stack)
            return self.efectuateOperation(op1)
        elif self.category == "ArrayOp" and self.value == "ArrConsult":
            op1 = self.arrayValue(stack)
            op2 = self.children[1].evalArithmeticExp(stack)
            if op1.checkIndex(op2):
                return op1[op2]
            else:
                print("Error de ejecución: Índice fuera de rango en operación consulta")
                sys.exit()
        elif self.category == "Exp":
            return self.children[0].evalArithmeticExp(stack)
        elif self.category == "Ident":
            return self.checkInitIdent(stack)
        elif self.category == "Literal":
            return self.getValue()
        else:
            print("El operador " + self.value + " no es válido en esta expresión")
            sys.exit()

    def evalBoolExp(self, stack):
        if isinstance(self, BinOpRelNode):
            op1 = self.children[0].evalArithmeticExp(stack)
            op2 = self.children[1].evalArithmeticExp(stack)
            return self.efectuateOperation(op1, op2)
        if isinstance(self, BinOpBoolNode):
            op1 = self.children[0].evalBoolExp(stack)
            op2 = self.children[1].evalBoolExp(stack)
            return self.efectuateOperation(op1, op2)
        if isinstance(self, BinOpEqualNode):
            if (self.getValue() == "ArithEqual" or self.getValue() == "ArithNequal"):
                op1 = self.children[0].evalArithmeticExp(stack)
                op2 = self.children[1].evalArithmeticExp(stack)
            else:
                op1 = self.children[0].evalBoolExp(stack)
                op2 = self.children[1].evalBoolExp(stack)
            return self.efectuateOperation(op1, op2)
        if isinstance(self, BoolOpNotNode):
            op1 = self.children[0].evalBoolExp(stack)
            return self.efectuateOperation(op1)
        elif self.category == "Exp":
            return self.children[0].evalBoolExp(stack)
        elif self.category == "Ident":
            return self.checkInitIdent(stack)
        elif self.category == "Literal":
            return getBoolean(self.getValue())
        else:
            print("El operador " + self.value + " no es válido en esta expresión")
            sys.exit()

    def evalArrayExp(self, stack):
        if self.category == "ArrayOp":
            if self.value == "ArrayAsig":
                return self.arrayValue(stack).getArrayItems()
            elif self.value == "ArrElementInit":
                newArray = []
                self.InitializeArray(stack, newArray)
                return newArray
        else:
            if self.category == "Ident":
                return self.checkInitIdent(stack)

    def evalArrayExpForPrint(self, stack):
        if self.category == "ArrayOp":
            if self.value == "ArrayAsig":
                return self.arrayValue(stack).getArrayItems()
            elif self.value == "ArrElementInit":
                newArray = []
                self.InitializeArray(stack, newArray)
                return newArray
        else:
            if self.category == "Ident":
                return self.checkInitIdentForPrint(stack)

    def evalGuard(self, stack, iterator=None):
        if self.children[0].children[0].evalBoolExp(stack):
            iterator[0] = True
            return self.children[1].evaluatorAux(stack)
        else:
            if (len(self.children) == 3):
                return self.children[2].evalGuard(stack, iterator)
            else:
                return True

    def evalDo(self, stack):
        iterator = [False]
        self.children[0].evalGuard(stack, iterator)
        while iterator[0]:
            iterator[0] = False
            self.children[0].evalGuard(stack, iterator)

        return True

    def evaluator(self):
        tableStack = []
        return self.evaluatorAux(tableStack)

    def evaluatorAux(self, stack):
        if isinstance(self, BlockNode):
            return self.evalBlock(stack)
        elif self.category == "Asig":
            return self.evalAsig(stack)
        elif self.category == "InstSequence":
            if len(self.children) == 2:
                return all([self.children[0].evaluatorAux(stack), self.children[1].evaluatorAux(stack)])
            else:
                return self.children[0].evaluatorAux(stack)
        elif self.category == "Read":
            return self.evalRead(stack)
        elif self.category == "For":
            return self.evalFor(stack, 0)
        elif self.category == "if":
            return self.children[0].evalGuard(stack)
        elif self.category == "do":
            return self.evalDo(stack)
        elif self.category == "print" or self.category == "println":
            if len(self.children) == 1:
                self.evalPrint(stack)
            else:
                return self.evalPrintAux(stack)
        elif self.category == "Concat":
            return self.evalConcat(stack)






    ############################################################################################################

    ################################################# GET Y SET ################################################

    ############################################################################################################

    ## Retorna el atributo value de un Node
    def getValue(self):
        return self.value

    ## Inserta un valor al atributo value de un Node
    ## Paramétro: newValue que corresponde al nuevo valor a insertar
    def setValue(self, newValue):
        self.value = newValue

## Creamos un objeto llamado DecNode el cual tendrá de herencia al objeto Node, pero que nos servirá para añadir información adicional
## y crear una distinción con los demás nodos. La principal característica es que tendrá el tupleList que corresponde a la lista de variable - tipo
## y con el cual construiremos las variables declaradas correspondientes.
class DecNode(Node):
    def __init__(self, category, value, tupleList, children=None, last=None):
        super().__init__(category, value, children)
        self.declaredVars = tupleList
        self.lastLine = last

    ## Retorna la tupleList que corresponde a las variables declaradas en el Nodo
    def getDeclaredVars(self):
        return self.declaredVars

    #Esto me permite que cada línea de declaración se vea como hija de la línea anterior. 
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

### Creamos un objeto llamado ForNode el cual tendrá de herencia al objeto Node, pero que nos servirá para añadir información adicional
## y crear una distinción con los demás nodos. La principal característica tendrá una tabla de simbolo de la variable de iteracción del For
class ForNode(Node):
    ## Construcción e inicialización del objeto ForNode
    def __init__(self, category, value, isFor, children=None, var=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table(isFor)
        self.symbol_table.fillTableFor(var)
        self.numIteraccion = 0
        
### Creamos un objeto llamado BlockNode el cual tendrá de herencia al objeto Node, pero que nos servirá para añadir información adicional
## y crear una distinción con los demás nodos. Tendrá una tabla de simbolo de las variables declaradas el bloque correspondiente.
class BlockNode(Node):
    ## Construcción e inicialización del objeto BlockNode
    def __init__(self, category, value, isFor, children=None, varList=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table(isFor)
        self.symbol_table.fillTable(varList)

    ## Verificamos que si el bloque tiene variables declaradas insertamos la nueva tabla de símbolos. De lo contrario solo chequeamos los errores estáticos de las instrucciones
    ## Luego para un bloque con variables declaradas chequeamos los errores estáticos si solo hay una instrucción y si hay varias, chequeamos el segundo y tercer hijo
    ## que corresponde a la instrucción y a la secuencia de instrucciones. Cabe resaltar que es necesario guardar el tamaño del stack ya que este puede variar dentro de la instrucción
    ## y luego tenemos que volver al stack al estado original en caso de alguna variación.
    def checkBlock(self, stack):
        if bool(self.symbol_table.getTable()):
            stack.insert(0, self.symbol_table)
            if (len(self.children) == 2):
                return self.children[1].checkStaticErrorsAux(stack)
            else:
                stackLength = len(stack)
                child1 = self.children[1].checkStaticErrorsAux(stack)
                while len(stack) != stackLength:
                    stack.pop(0)
                child2 = self.children[2].checkStaticErrorsAux(stack)

                stack.pop(0)

                return child1 and child2
        else:
            return self.children[0].checkStaticErrorsAux(stack)

    def evalBlock(self, stack):
        if bool(self.symbol_table.getTable()):
            stack.insert(0, self.symbol_table)
            if (len(self.children) == 2):
                return self.children[1].evaluatorAux(stack)
            else:
                stackLength = len(stack)
                child1 = self.children[1].evaluatorAux(stack)
                while len(stack) != stackLength:
                    stack.pop(0)
                child2 = self.children[2].evaluatorAux(stack)

                stack.pop(0)

                return child1 and child2

        else:
            return self.children[0].evaluatorAux(stack)

class BinOpNode(Node):

    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op1, op2):
        if self.getValue() == "Plus":
            self.result = op1 + op2
        elif self.getValue() == "Minus":
            self.result = op1 - op2
        elif self.getValue() == "Mult":
            self.result = op1 * op2
        elif self.getValue() == "Div":
            self.result = op1 // op2
        elif self.getValue() == "Mod":
            self.result = op1 % op2

        return self.result
        
class UnaryMinusNode(Node):

    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op):
        self.result = -1 * op
        return self.result

class FunctionNode(Node):
    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op):
        if self.value == "atoi":
            self.result = op[op.getMin()]
        elif self.value == "max":
            self.result = op.getMax()
        elif self.value == "min":
            self.result = op.getMin()
        else:
            self.result = op.getLength()

        return self.result

class BinOpRelNode(Node):

    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op1, op2):
        if self.getValue() == "Geq":
            self.result = (op1 > op2 or op1 == op2)
        elif self.getValue() == "Greater":
            self.result = op1 > op2
        elif self.getValue() == "Leq":
            self.result = (op1 < op2 or op1 == op2)
        elif self.getValue() == "Less":
            self.result = op1 < op2

        return self.result

class BinOpBoolNode(Node):

    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op1, op2):
        if self.getValue() == "Or":
            self.result = op1 or op2
        elif self.getValue() == "And":
            self.result = op1 and op2

        return self.result

class BinOpEqualNode(Node):

    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op1, op2):
        if self.getValue() == "ArithEqual" or self.getValue() == "BoolEqual":
            self.result = op1 == op2
        else:
            self.result = op1 != op2

        return self.result

class BoolOpNotNode(Node):
    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.result = None

    def efectuateOperation(self, op):
        self.result = not op
        return self.result
        
class PrintNode(Node):

    def __init__(self, category, value, children=None):
        super().__init__(category, value, children)
        self.elementToPrint = ""

    def buildPrint(self, newElement):
        if(newElement != None):
            self.elementToPrint = self.elementToPrint + newElement
        else: 
            print("Error construyendo el print")
        
    def println(self):
        if(self.elementToPrint != None):
            print(self.elementToPrint)
        else: 
            print("Lo que se quiere imprimir está vacío")
        self.elementToPrint = ""

    def print(self):
        if(self.elementToPrint != None):
            print(self.elementToPrint, end='')
        else: 
            print("Lo que se quiere imprimir está vacío")
        self.elementToPrint = ""
