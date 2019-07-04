#!/usr/bin/python

""" TP2 para ejercitar sincronizacion y sus problemas"""
import threading
import time
import random
import multiprocessing
import os

FAN = 1

lugares_bote = []
viajes = 0
nb_places = threading.BoundedSemaphore(4)
SEMAPHORE = 4
condition = threading.Event()


def check_PSG_OM_in_bote(liste):
	PSG = 0
	OM = 0
	result = []
	for i in liste :
		if i == "PSG" :
			PSG += 1
		if i == "OM" :
			OM += 1
	result.append(PSG)
	result.append(OM)
	return result


def a_bordo():
	global lugares_bote, SEMAPHORE
	nb_places.acquire()
	SEMAPHORE -= 1
	if len(lugares_bote) == 4:
		a_remar()


def a_remar():
	global lugares_bote
	global viajes
	global nb_places, SEMAPHORE
	print "soy el capitan del viaje ",viajes," y me voy con mi embarcacion y tres companeros\n"
	lugares_bote = []
	nb_places.release()
	viajes += 1
	nb_places = threading.BoundedSemaphore(4)
	SEMAPHORE = 4
	condition.set()
	

def entrar_validation(hincha):
	global lugares_bote
	global FAN, SEMAPHORE
	FAN += 1
	fan = FAN
	if hincha == "PSG":
		while 1 :	
			boat = check_PSG_OM_in_bote(lugares_bote)
			if boat == [2,1]  or boat == [0,3] :
				print "Oh no puedo entrar, espero !!!!",fan
				condition.wait()
				condition.clear()
			else :
				lugares_bote.append("PSG")
				print "Ici c'est Paris !Vamos PSG !",lugares_bote ,fan," ",SEMAPHORE
				a_bordo()
				break
	elif hincha == "OM":
		while 1 :
			boat = check_PSG_OM_in_bote(lugares_bote)
			if boat == [1,2]  or boat == [3,0] :
				print "Oh no puedo entrar,espero !!!!",fan
				condition.wait()
				condition.clear()
			else :
				lugares_bote.append("OM")
				print "Droit au But!Vamos OM !", lugares_bote,fan," ",SEMAPHORE
				a_bordo()
				break
	else :
		print "Ninguna hincha quiere ver la partida ?"
	


def Hinchada_PSG():
    	""" Generacion de hinchas de PSG"""
	while 1:
	        time.sleep(random.randrange(1, 5))
        	mq.put("PSG")
		if quit.get() == True :
			break 
	

def Hinchada_OM():
	""" Generacion de hinchas de OM"""
	while 1:
	        time.sleep(random.randrange(1, 5))
	        mq.put("OM")
		if quit.get() == True :
			break
	
	
def Coordinador():
	global viajes 
	threads = []
	while viajes < 20:
		quit.put(False)
		quit.put(False)
		hincha = mq.get()
		print hincha
		threads.append(threading.Thread(target = entrar_validation, args = (hincha,)))
		threads[len(threads) - 1].start()
	for i in range(len(threads)):
		threads[i].join()
	quit.put(True)
	quit.put(True)
		

p1 = multiprocessing.Process(target = Hinchada_PSG)
p2 = multiprocessing.Process(target = Hinchada_OM)
p3 = multiprocessing.Process(target = Coordinador)

mq = multiprocessing.Queue()
quit = multiprocessing.Queue()

p1.start()
p2.start()
p3.start()

p3.join()
print("terminaron los viajes ")
p1.join()
print "jamin"
p2.join()
print "haouioui"
