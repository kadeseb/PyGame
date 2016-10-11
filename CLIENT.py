#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Programme client
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import sys
import socket
import network as Network

print '**********************'
print '* PyBlague Client v1 *'
print '**********************'

# Contrôle des arguments
if len( sys.argv ) < 3:
	print 'Usage: CLIENT.py <serveur> <port>'
	print ''
	print 'server: Adresse du serveur'
	print 'port: \tPort en écoute sur le serveur'
	exit( 1 )

server = sys.argv[1]
port = sys.argv[2]

# Contrôle du port
if( not Network.portIsValid( port ) ):
	print '-> [Erreur] Le port spécifé est invalide !'
	exit( 1 )
else:
	port = int( port )

print '-> Tentative de connexion à %s:%d' % (server, port)

client = Network.Client( server, port )

if( not client.isConnected() ):
	print '-> [Erreur] Connection refusé !'
	exit( 1 )

print '-> Connecté !'

while True:
	command = raw_input( '#> ' )
	command = command.upper()

	if not client.sendCommand( command ):
		print '-> [Erreur] Connexion interrompu !'
		exit( 0 )

	response = client.getResponse()
	if len(response) > 0:
		response = response.split( '\n' )

		for line in response:
			print '|> %s' % line

	if( command == 'E' or command == 'EXIT' ):
		exit(0)
