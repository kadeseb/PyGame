#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Gère le réseau
# Crée le:	10/10/2016
# ========================================
import urllib
import json
import socket
import threading
import types
import hashlib
from config import *
from command import *
from functions import *
from protocol import *

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
		if DEBUG: print '| Création du socket'
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
		if DEBUG: print '$ Ok'

		# Initialisation de l'objet
		self.clientSessionList = []
		self.manager = manager

		print '| Serveur en écoute sur %d\n' % CONFIG['PORT']
		print '-'*10 + 'JOURNAL' + '-'*10

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

		self.disconnect = False
		self.authentified = False
		self.clientsocket = clientsocket
		self.ip = ip
		self.port = port
		self.manager = manager

	# Lance le thread
	def run( self ):
		print '[+]{ %s:%d } Connexion' % ( self.ip, self.port )

		while not self.manager.exiting():
			if( self.disconnect ): 			break;
			elif( not self.authentified ): 	self.login()
			else: 							self.handleCommand()
		print '[+]{ %s:%d } Déconnexion' % ( self.ip, self.port )
		self.clientsocket.close()

	# Analyse la requête
	#
	# -?-
	# [dict] request:	Requête
	# -!-
	# [bool]
	def handleCommand( self ):
		# ---------------------------
		# Récupération de la commande
		# ---------------------------
		exchange = Exchange()
		exchange.recv( self.clientsocket )

		try:
			command = exchange.get( 'COMMAND' )
			print '[~]{ %s:%d } %s' % ( self.ip, self.port, command )
		except KeyError:
			return False

		'''
		<!> Penser à implémenter ça de façon moins deg
		'''
		if( command == 'exit' ):
			self.disconnect = True

		# ************************
		# Execution de la commande
		# ************************
		commandID = self.manager.put( command )
		result = None

		while not result:
			result = self.manager.get( commandID )

		# -------------------
		# Envoie de la sortie
		# -------------------
		exchange.purge()
		exchange.add( 'MODE', 'COMMANDRESPONSE' )
		exchange.add( 'STATUS', result['STATUS'] )
		exchange.add( 'OUTPUT', result['OUTPUT'] )
		exchange.send( self.clientsocket )

		return True

	def login( self ):
		exchange = Exchange()

		# ----------------------------------
		# Récupération de la demande de salt
		# ----------------------------------
		exchange.recv( self.clientsocket )

		# --------------
		# Envoie du salt
		# --------------
		salt = randomAlphaNumStr( CONFIG['SALTSIZE'] )

		exchange.purge()
		exchange.add( 'MODE', 'SENDSALT' )
		exchange.add( 'SALT', salt )
		exchange.send( self.clientsocket )

		# ---------------------------------
		# Récupération du mot de passe salé
		# ---------------------------------
		exchange.recv( self.clientsocket )

		try:
			saltedPass = exchange.get( 'PASS' )
		except KeyError:
			return False

		# ----------------
		# Envoie du status
		# ----------------
		validSaltedPass = hashlib.sha1( CONFIG['PASSWORD'] + salt ).hexdigest()
		validPassword = saltedPass == validSaltedPass

		exchange.purge()
		exchange.add( 'MODE', 'LOGINSTATUS' )
		exchange.add( 'STATUS', validPassword )
		exchange.send( self.clientsocket )

		if( validPassword ):
			self.authentified = True
			print '[#]{ %s:%d } Authentification réussie' % ( self.ip, self.port )
		else:
			print '[#]{ %s:%d } Authentification échoué' % ( self.ip, self.port )


#######################
# Session côté client #
#######################
class ClientSession:
	def __init__( self ):
		self.password = None
		self.connected = False
		self.authentified = False

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
		exchange = Exchange()

		# ----------------------------
		# Envoie de la demande de salt
		# ----------------------------
		exchange.purge()
		exchange.add( 'MODE', 'ASKSALT' )
		exchange.send( self.socket )

		# --------------------
		# Récupération du salt
		# --------------------
		exchange.recv( self.socket )

		try:
			salt = exchange.get( 'SALT' )
		except KeyError:
			return False

		# ----------------------
		# Envoie du mot de passe
		# ----------------------
		saltedPass = hashlib.sha1( password + salt ).hexdigest()

		exchange.purge()
		exchange.add( 'MODE', 'LOGIN' )
		exchange.add( 'PASS', saltedPass )
		exchange.send( self.socket )

		# --------------------------
		# Récupération de la réponse
		# --------------------------
		exchange.recv( self.socket )

		try:
			self.authentified = exchange.get( 'STATUS' )
		except KeyError:
			return False

		return self.authentified

	# Envoie une commande et retourne la réponse
	#
	# -?-
	# [str] command
	# -!-
	# [dict] / [bool(false)]:	Retourne le résultat de la commande ou False si une erreur survient
	def sendCommand( self, command ):
		if( not self.connected or not self.authentified ):
			return False

		if( command == 'quit' or command == 'exit' ):
			self.connected = False

		exchange = Exchange()

		# ---------------------
		# Envoie de la commande
		# ---------------------
		exchange.purge()
		exchange.add( 'COMMAND', command )
		exchange.send( self.socket )

		# -----------------------
		# Réception de la réponse
		# -----------------------
		exchange.recv( self.socket )

		try:
			return {
				'STATUS': exchange.get( 'STATUS' ),
				'OUTPUT': exchange.get( 'OUTPUT' )
			}
		except KeyError:
			return False

	def connectionClosed( self ):
		return not self.connected
