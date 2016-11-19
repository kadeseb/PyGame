#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Gère le réseau
# Auteur:	kadeseb
# Crée le:	10/10/2016
# ----------------------------------------
import urllib
import json
import socket
import threading
import types
import hashlib
from config import *
from command import *
from functions import *

class Server( threading.Thread ):
	# Démarre le serveur
	#
	# -?-
	# [Manager] manager:	Instance de Manager
	# -$-
	# TypeError				Si <manager> n'est pas de type Manager
	def __init__( self, manager ):
		threading.Thread.__init__( self )

		# Création du socket
		print '| Création du socket'
		try:
			self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			self.socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
			self.socket.bind( ("", CONFIG['PORT'] ) )
			self.socket.listen( 10 )
			self.socket.settimeout( CONFIG['TIMEOUT'] )
			#self.socket.setblocking( 0 )
		except socket.error:
			print '$ ERREUR: La création du socket à échoué !'
			raise SystemError()
		print '$ Ok'

		# Initialisation de l'objet
		self.clientSessionList = []
		self.manager = manager

		print '| Serveur en écoute sur %d\n' % CONFIG['PORT']
		print ' '

	# Met le serveur en état d'écoute
	def listen( self ):
		# Acceptation des connexions entrantes
		try:
			(clientsocket, (ip, port)) = self.socket.accept()
		except socket.error:
			return

		# Création du thread client
		session = ServerSession( ip, port, clientsocket, self.manager )
		session.start()
		self.clientSessionList.append( session )

	# Lance le thread
	def run( self ):
		while not self.manager.exiting():
			self.listen()

		self.clientSessionList = None

########################
# Session côté serveur #
########################
class ServerSession( threading.Thread ):
    # Créer une nouvelle session
    #
    # -?-
    # [socket]  clientsocket:   Socket à utiliser
	def __init__( self, ip, port, clientsocket, manager ):
		threading.Thread.__init__( self )

		self.authentified = False
		self.clientsocket = clientsocket
		self.ip = ip
		self.port = port
		self.manager = manager

	# Lance le thread
	def run( self ):
		print '[+]{ %s: %d } Connexion d\'un client ' % ( self.ip, self.port )

		while not self.manager.exiting():
			try:
				request = self.clientsocket.recv( CONFIG['NTWBUFSIZE'] )

				try:
					request = json.loads( request )
				except ValueError:
					break

				self.handleRequest( request )
			except socket.error:
				break

		print '[+]{ %s: %d } Déconnexion' % ( self.ip, self.port )
		self.clientsocket.close()

	# Analyse la requête
	#
	# -?-
	# [dict] request:	Requête
	# -!-
	# [bool]
	def handleRequest( self, request ):
		if( not 'CODE' in request and not 'DATA' in request  ):
			return False

		cmdID = self.manager.put( request['DATA'] )

		while True:
			response = self.manager.get( cmdID )

			if( response ):
				cmdOutput = json.dumps( response )
				self.clientsocket.send( cmdOutput )
				break

#######################
# Session côté client #
#######################
class ClientSession:
    def __init__( self ):
        self.password = None
        self.connected = False
        self.loged = False

    # Se connecte à un serveur
    #
    # -?-
    # [str] hostname
    # [int] port
    # -!-
    # [bool]
    def connect( self, hostname, port ):
        if( not portIsValid( port ) ):
            return False

        try:
            self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.socket.settimeout( CONFIG['TIMEOUT'] )
            self.socket.connect( (hostname, port) )
        except socket.error:
            self.connected = False
            return False

        self.connected = True
        return True

    # S'identifie auprès du serveur
    #
    # -?-
    # [str] password:   Mot de passe
    # -!-
    # [bool]
    def login( self, password ):
        self.socket.send( 'test' )
        return True

    # Envoie une commande et retourne la réponse
    #
    # -?-
    # [str] command
    # -!-
    # [dict] / [bool(false)]:	Retourne le résultat de la commande ou False si une erreur survient
    def sendCommand( self, command ):
		if( not self.connected ):
			return False

		# Envoie de la requête
		request = { 'CODE': 2, 'DATA': command }
		request = json.dumps( request )

		try:
			self.socket.send( request )
		except socket.error:
			return False

		# Récupération de la réponse
		try:
			response = self.socket.recv( CONFIG['NTWBUFSIZE'] )
		except socket.error:
			return False

		try:
			return json.loads( response )
		except ValueError:
			return False
