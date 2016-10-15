#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Programme client
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import sys
import network as Network
from docopt import docopt

help = '''
Usage:
	CLIENT.py <serveur> [port]

Options
	-h --help	Affiche l'aide.
	--version  	Affiche la version.
'''

if __name__ == '__main__':
	arguments = docopt( help, version='PyJoke Client 1.0' )

	#///////////////////////////
	# Extraction des arguments /
	#///////////////////////////
	server = arguments['<serveur>']

	if not arguments['port']:
		port = 2048
	elif( not Network.portIsValid( arguments['port'] ) ):
		print '-> [Erreur] Le port spécifié est invalide !'
		exit( 1 )
	else:
		port = int( arguments['port'] )

	#/////////////////////////
	# Execution du programme /
	#/////////////////////////
	print '**********************'
	print '* PyBlague Client v1 *'
	print '**********************'
	print '-> Tentative de connexion à %s:%d' % (server, port)

	client = Network.Client( server, port )
	if( not client.isConnected() ):
		print '-> [Erreur] Connection refusé !'
		exit( 1 )
	else:
		print '-> Connecté !'
		print '======================'


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
