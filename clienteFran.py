#Fundamentos de Internet 2018/2019
#Trabajo Final
#Autor: Francisco Javier Romero Rojo

#Modulos importados

import socket 
import sys
import os
import os.path
import random
import select

#Variables usadas

IpServer = sys.argv[1]
PortServer = 55000
RandomPort = str(random.randint(45000, 55000))
message2 = 'LISTA'

#Comprobacion del numero de argumentos

if len(sys.argv) > 3:
	print 'Error. Uso: cliente IP [fichero]'
	sys.exit()

#Registro del cliente

if len(sys.argv) == 2:
	message1 = RandomPort
	socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Solicitando registro en el servidor con el puerto: '+ message1
	socketUDP.sendto(message1, (IpServer, PortServer))
	rlist, wlist, elist = select.select([socketUDP], [], [], 3)
	if [rlist, wlist, elist] == [[], [], []]:
		print 'Error: no hay respuesta por parte del servidor '+ IpServer +' en el puerto '+ str(PortServer)
		socketUDP.close()
		sys.exit()
	else:
		answer, address = socketUDP.recvfrom(100)
		print 'Respuesta del servidor: '+ answer		
		socketUDP.close()
		
		#Socket TCP escuchando
	
		socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socketTCP.bind(('', int(message1)))
		print 'Estableciendo socket TCP de escucha en el puerto: '+ message1 
		socketTCP.listen(10)
		conn, addr = socketTCP.accept()
		while 1:
			data = conn.recv(1024)
			if data != '.' and len(data) > 0:		
				conn.sendall('ok')
				nameFilename, sizeFilename = data.split(' ')
				content = conn.recv(int(sizeFilename))
				fout = open(nameFilename, 'w')
				fout = write(content)
				fout.close()
				conn.sendall('transfer done')
				
				
		

#Comprobacion del fichero y replica del mismo

if len(sys.argv) == 3:
	filename = sys.argv[2]
	message1 = RandomPort
	if os.path.isfile(filename) == False:
		print 'Error. Fichero '+ filename +' inexistente'
		sys.exit()
	else:
		socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'Realizando peticion de LISTA al servidor'
		socketUDP.sendto(message2, (IpServer, PortServer))
		rlist, wlist, elist = select.select([socketUDP], [], [], 3)
		if [rlist, wlist, elist] == [[], [], []]:
			print 'Error: no hay respuesta por parte del servidor '+ IpServer +' en el puerto '+ str(PortServer)
			socketUDP.close()
			sys.exit()
		else:
			ReturnedList, address = socketUDP.recvfrom(1024)
			LIST = ReturnedList.split(';')
			print 'Lista: '+ str(LIST) +' recibida por parte del servidor'
			for clientA in LIST:
				ipA, portA = clientA.split(',')
				datalist = filename+ ' ' + str(os.stat(filename).st_size)
				if portA != message1:
					socketTCP2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					try:
						socketTCP2.connect((ipA, int(portA)))
						socketTCP2.sendall(datalist)	
						if socketTCP2.recv(1024) == 'ok':
							Fcontent = open(filename)
							Archive = Fcontent.read()
							Fcontent.close()
							if socketTCP2.recv(1024) == 'transfer done':
								socketTCP2.close()
								print 'Transferencia correcta'					
					except socket.error:
						print 'Error: no se realiza la conexion con el cliente '+ ipA +' : '+ portA
	
					#Registro del cliente
	
					socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					print 'Solicitando registro en el servidor con el puerto: '+ message1
					socketUDP.sendto(message1, (IpServer, PortServer))
					rlist, wlist, elist = select.select([socketUDP], [], [], 3)
					if [rlist, wlist, elist] == [[], [], []]:
						print 'Error: no hay respuesta por parte del servidor '+ IpServer +' en el puerto '+ str(PortServer)
						socketUDP.close()
						sys.exit()
					else:
						answer, address = socketUDP.recvfrom(100)
						print 'Respuesta del servidor: '+ answer		
						socketUDP.close()
