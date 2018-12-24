import select
import sys
import os.path
import socket
import random

serverIp = sys.argv[1]
serverPort = 55000
bindPort = str(random.randint(45000, 55000))
a = []  # Empty array


def timeout(c, i, p, t, b, s):
    r, w, e = select.select([c], a, a, t)
    if [r, w, e] == [a, a, a]:
        if s == 0:
            print 'Error: no hay respuesta por parte del servidor ' + i + ' en el puerto ' + str(p)
        else:
            print 'Error: no hay respuesta por parte del cliente ' + i + ' en el puerto ' + str(p)
        sys.exit()
    else:
        return c.recv(b)


def register():
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.sendto(bindPort, (serverIp, serverPort))
    timeout(c, serverIp, serverPort, 3, 1024, 0)
    return c


if len(sys.argv) == 2:
    client = register()
    transfer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer.bind(('127.0.0.1', int(bindPort)))
    transfer.listen(10)
    while 1:
        tunnel, address = transfer.accept()
        data = tunnel.recv(1024)
        if data != '.' and len(data) > 0:
            tunnel.sendall('ok')
            name, size = data.split(' ')
            content = tunnel.recv(int(size))
            fileContent = open(name, 'w')
            fileContent.write(content)
            fileContent.close()
            tunnel.sendall('transfer done')
            tunnel.close()

if len(sys.argv) == 3:
    filePath = sys.argv[2]
    if not os.path.isfile(filePath):
        print 'Error. Fichero ' + filePath + 'inexistente'
        sys.exit()
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto('LISTA', (serverIp, serverPort))
        data = timeout(client, serverIp, serverPort, 3, 1024, 0)
        array = data.split(';')
        for element in array:
            if element:
                ip, port = element.split(',')
                data = filePath + ' ' + str(os.stat(filePath).st_size)
                req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    req.connect((ip, int(port)))
                    req.sendall(data)
                    if timeout(req, ip, port, 3, 100, 1) == 'ok':
                        fileContent = open(filePath)
                        req.sendall(fileContent.read())
                        fileContent.close()
                        if timeout(req, ip, port, 10, 100, 1) == 'transfer done':
                            req.close()
                except socket.error:
                    print 'Error: no se ha podido connectar con el cliente ' + ip + ' en el puerto ' + port
        register()

else:
    print 'Error. Uso: cliente IP [Fichero]'
    sys.exit()
