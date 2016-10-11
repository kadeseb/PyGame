#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gère la partie réseau
# Auteur:	kadeseb
# Crée le:	10/10/2016
# ----------------------------------------
import socket
import threading
import types
from config import *
from action import Manager

##
# Vérifie si un port est valide
# -?-
# [int/string] port 	Port à tester
# -!-
# [bool]				Le port est valide
##
def portIsValid( port ):
	if( not isinstance( port, int ) and not isinstance( port, str ) ):
		return False

	if( isinstance( port, str ) ):
		try:
			port = int( port )
		except ValueError:
			return False

	return ( port > 0 ) and ( port < 65535 )

#------------------
# Gère le serveur -
#------------------
class Server( threading.Thread ):
	def __init__( self, manager ):
		threading.Thread.__init__( self )

		# Création du socket
		self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		self.socket.bind( ("", CONFIG['PORT'] ) )
		self.socket.listen( 10 )
		self.socket.setblocking( 0 )

		# Initialisation de l'objet
		self.clientThreadList = []
		self.manager = manager

		print '-> Serveur en écoute sur %d\n' % CONFIG['PORT']

	def listen( self ):
		# Acceptation des connexions entrantes
		try: 
			(clientsocket, (ip, port)) = self.socket.accept()
		except socket.error:
			return False

		# Création du thread client
		thread = ClientThread( ip, port, clientsocket, self.manager )
		thread.start()
		self.clientThreadList.append( thread )

		return True

	def run( self ):
		while not self.manager.askExit():
			self.listen()

class ClientThread( threading.Thread ):
    def __init__( self, ip, port, clientsocket, manager ):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.manager = manager

    def run( self ): 
        print '[+]{%s:%d} Connexion d\'un client' % ( self.ip, self.port)

        while True:
        	command = self.clientsocket.recv( 512 )

        	print '[~]{%s:%d} %s' % ( self.ip, self.port, command)

        	if( command == 'E' or command == "EXIT" or self.manager.askExit() ):
        		self.clientsocket.send( 'DECONNEXION' )
        		break
        	else:
	        	self.manager.execute( command )
	        	self.clientsocket.send( self.manager.getResponse() )

        print '[-]{%s:%d} Déconnexion' % ( self.ip, self.port )

class Client():
	## 
	# Constructeur
	##
	def __init__( self, address, port ):
		try:
			self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			self.socket.settimeout( CONFIG['TIMEOUT'] )
			self.socket.connect( (address, port) )

		except socket.error:
			self.connectionOk = False
			return

		self.connectionOk = True

	##
	# Envoie une commande vers le serveur
	# -?- 
	# [string] Commande 	La commande à exécuter
	##
	def sendCommand( self, command ):
		try:
			self.socket.send( command.encode() )
			self.response = self.socket.recv( 512 )
		except socket.error:
			return False
		return True

	##
	# Retourne la réponse renvoyé par le serveur
	##
	def getResponse( self ):
		return self.response

	##
	# Permet de connaître l'état de la connexion
	# -!-
	# [bool]	Le client est connecté
	##
	def isConnected( self ):
		return self.connectionOk
