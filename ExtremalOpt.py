#!/usr/bin/python
# -*- coding: utf-8 -*-
# Programa Cliente

import sys
import random
import re
import copy

class Objeto: #CASO DE PRUEBA EXTRAIDO DE EXCEL
    def __init__(self):
        self.nombre = ""
        self.id = []
        self.peso = []
        self.precio = []
        self.limitePeso = 0
        self.tamano = 0
        self.pesoTotal = 0
        self.precioTotal = 0

    def imprime(self):
        print("id:", self.id,"peso:",self.peso, "precio:", self.precio)

    def agregarObjeto(self,id,peso,precio):
        self.id.append(id)
        self.peso.append(peso)
        self.precio.append(precio)
        self.pesoTotal += precio
        self.pesoTotal += peso

    def setNombre(self,nombre):
        self.nombre = nombre
    def setLimite(self,limite):
        self.limitePeso = limite
    def setTam(self,tam):
        self.tamano = tam

class Solucion:
    def __init__(self):
        self.indice = []
        self.estado = []
        self.peso = []
        self.precio = []
        self.fitness = []
        self.precioTotal = 0
        self.pesoTotal = 0
        self.factible = bool

    def ordenarPeorAMejor(self):
        for numPasada in range(len(self.fitness) - 1, 0, -1):
            for i in range(numPasada):
                if self.fitness[i] > self.fitness[i + 1]:
                    temp = self.fitness[i]
                    temp2 = self.indice[i]
                    temp3 = self.estado[i]
                    temp4 = self.peso[i]
                    temp5 = self.precio[i]
                    self.fitness[i] = self.fitness[i + 1]
                    self.indice[i] = self.indice[i + 1]
                    self.estado[i] = self.estado[i + 1]
                    self.peso[i] = self.peso[i + 1]
                    self.precio[i] = self.precio[i + 1]
                    self.fitness[i + 1] = temp
                    self.indice[i + 1] = temp2
                    self.estado[i + 1] = temp3
                    self.peso[i + 1] = temp4
                    self.precio[i + 1] = temp5

    def conteoUnosEstado(self):
        suma = 0
        for x in range(len(self.estado)):
            if(self.estado[x]==1):
                suma += 1
        return suma

    def verTodo(self):
        print("Indice:",self.indice, "\nEstado o solucion:", self.estado, "\nPrecio", self.precio, "\nPeso", self.peso, "\nFitness", self.fitness, "\nPrecio Total:",self.precioTotal,"\nPeso Total:",self.pesoTotal,"\nFactibilidad:",self.factible)

def numRandomicoReal():
    return random.random()

def numRandomicoUnoToN(N):
    return random.randint(1, N)

def initEcosistema(objetos):
    tmp = Solucion()
    tmp.precio = objetos.precio
    tmp.peso = objetos.peso
    evaluarFitnessEspecie(tmp)
    for x in range (0,objetos.tamano):
        if(numRandomicoUnoToN(2)<=1):
            tmp.estado.append(1)
        else:
            tmp.estado.append(0)
        tmp.indice.append(x+1)
    random.shuffle(tmp.estado)
    return tmp

def evaluarFitnessEspecie(tmp):
    for x in range(len(tmp.peso)):
        tmp.fitness.append(tmp.precio[x] / tmp.peso[x])
    return tmp

def selecEspecieRuleta(valores):
    seleccion = 0
    seleccionAleatorio = numRandomicoReal()
    for x in range(len(valores)):
        if (x == 0):
            if (seleccionAleatorio < valores[x]):
                seleccion = x
        else:
            if seleccionAleatorio > valores[x - 1] and seleccionAleatorio < valores[x]:
                seleccion = x
    return seleccion  # devuelvo el individuo seleccionado

def reemplazoEspecie(vectorProb, primeraSolucion):
    seleccion = selecEspecieRuleta(vectorProb)
    #while (primeraSolucion.estado[seleccion] == 0):  # Esta condicion la he agregado yo, Pero genera problemas a la larga... que hacer...
    #    seleccion = selecEspecieRuleta(vectorProb)
    primeraSolucion.estado[seleccion] = 0

    cambio = numRandomicoUnoToN(50) - 1
    while (cambio == seleccion):
        cambio = numRandomicoUnoToN(50) - 1
    if(primeraSolucion.estado[cambio] == 1):
        primeraSolucion.estado[cambio] = 0
    else:
        primeraSolucion.estado[cambio] = 1


def generarVectorProb(tamano):
    vectorProb = []
    suma=0
    for x in range(tamano):
        vectorProb.append((x+1)**(-tau))
        suma += vectorProb[x]
    for x in range(tamano):
        vectorProb[x] = vectorProb[x]/suma
    for x in range(tamano):
        vectorProb[x] = vectorProb[x-1]+vectorProb[x]
    return vectorProb

def evaluarEcosistema(ecosistema,objetos):
    ecosistema.precioTotal = 0
    ecosistema.pesoTotal = 0
    for x in range(objetos.tamano):
        if(ecosistema.estado[x] == 1):
            ecosistema.precioTotal += ecosistema.precio[x]
            ecosistema.pesoTotal += ecosistema.peso[x]
    if(ecosistema.pesoTotal <= objetos.limitePeso):
        ecosistema.factible = True
    else:
        ecosistema.factible = False
    return ecosistema.factible

def lecturaArchivo(path):
    data = Objeto()
    with open(path) as f:
        for line in f.readlines()[0:]:
            b = re.split(',|\n| ',line)
            if(b[0] == ('n')):
                data.setTam(int(b[1]))
            elif (b[0] == ('c')!=-1):
                data.setLimite(int(b[1]))
            elif (b[0] == ('z')!=-1):
                NoUtil = int(b[1]) # este dato es el valor a alcanzar $$ es el mejor... pero no lo utilizaremos.
            elif(b[0].find('knapPI')!=-1):
                data.setNombre(b[0])
            elif(b[0] == ('time')!=-1):
                NoUtil = b[1]  # este dato es el tiempo, pero siempre es cero... no lo utilizaremos.
            else:
                if(b[0].find('---')!=-1):
                    break
                data.agregarObjeto(int(b[0]),int(b[1]),int(b[2]))
    return data

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("No ha ingresado todos los parametros solicitados.")
        sys.exit(0)

    #INICIALIZACION

    objetosMochila = lecturaArchivo(sys.argv[1]) #Archivo de entrada procesado
    semilla = int(sys.argv[2]) #Semilla
    condTermOnumIts = int(sys.argv[3]) #Condicion de termino o numero de iteraciones
    tau = float(sys.argv[4]) #Probabilidad
    xBest = 0

    random.seed(semilla)  # Asignamos la semilla al random.
    primeraSolucion = initEcosistema(objetosMochila)
    if(evaluarEcosistema(primeraSolucion,objetosMochila)):
        xBest = copy.copy(primeraSolucion)
    vectorProb = generarVectorProb(objetosMochila.tamano)

    for x in range(condTermOnumIts):
        primeraSolucion.ordenarPeorAMejor() #Se rankea y ordena del peor al mejor
        reemplazoEspecie(vectorProb, primeraSolucion) #Se hace el reemplazo
        if(evaluarEcosistema(primeraSolucion,objetosMochila)):
            if(xBest == 0):
                xBest = copy.copy(primeraSolucion)
            if(xBest.precioTotal<primeraSolucion.precioTotal):
                xBest = copy.copy(primeraSolucion)

    if(xBest == 0):
        print("NO se pudo encontrar una solucion FACTIBLE")
    else:
        print("La solucion encontrada es la siguiente:\n")
        xBest.verTodo()









