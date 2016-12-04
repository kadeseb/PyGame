#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ==========================
# Projet:	PyBlague
# Rôle:		Programme client
# Crée le:	09/10/2016
# ==========================
import network as Network
from functions import *
from config import *
from docopt import docopt
import getpass

format = '''
Usage:
	CLIENT.py <serveur> [<port>]

Options:
	--help					Affiche ce message et quite le programme
'''

if __name__ == '__main__':
	print '########################################'
 	print '#  _____            _       _          #'
 	print '# |  __ \          | |     | |         #'
 	print '# | |__) |   _     | | ___ | | _____   #'
 	print '# |  ___/ | | |_   | |/ _ \| |/ / _ \\  #'
 	print '# | |   | |_| | |__| | (_) |   <  __/  #'
 	print '# |_|    \__, |\____/ \___/|_|\_\___|  #'
	print '#        __/ |                         #'
	print '#       |___/  Client v.2              #'
	print '#                                      #'
	print '########################################'

	arguments = docopt( format, version='PyJoke Client 1.0', options_first=False )
	hostname = arguments['<serveur>']
	port = arguments['<port>']

	if( port ):
		if( portIsValid( port ) ):
			port = int( port )
		else:
			print '-> [Erreur] Port invalide !'
			exit( 1 )
	else:
		port = CONFIG['PORT']

	#/////////////////////////
	# Execution du programme /
	#/////////////////////////
	print '<> SERVEUR %s:%d' % ( hostname, port )

	session = Network.ClientSession()
	connected = session.connect( hostname, port )

	if( not connected ):
		print '-> [ERREUR]: Connection refusé !'
		exit( 1 )
	else:
		print '-> Connecté !'

	##########################
	# Saisie du mot de passe #
	##########################
	validAuth = False
	tryCount = 0

	while not validAuth:
		if( tryCount >= 3 ):
			exit( 1 )

		password = getpass.getpass( '-> Mot de passe: ' )

		if( session.login( password ) ):
			validAuth = True

		print '_'*40
		print ':) AUTHENTIFICATION REUSSIE !' if validAuth else ':( AUTHENTIFICATION ECHOUE !'
		print '_'*40

		tryCount += 1

	while True:
		try:
			command = raw_input( '#> ' )
			response = session.sendCommand( command )

			print '| Status:', response['STATUS']
			print '| ' + '-'*60

			for line in response['OUTPUT'].split( '\n' ):
				print '| ', line

			if( session.connectionClosed() ):
				exit( 0 )
		except KeyboardInterrupt:
			print 'Stop'
			exit( 0 )
