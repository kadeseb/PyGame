#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ----------------------------------------
# Projet:	PyBlague
# Rôle:		Programme local de test
# Auteur:	kadeseb
# Crée le:	09/10/2016
# ----------------------------------------
import command

commandManager = command.Manager()
commandManager.associate( 'quit', 'Command_Quit' )
commandManager.associate( 'help', 'Command_Help' )
commandManager.associate( 'eject', 'Command_Eject' )
commandManager.associate( 'sound', 'Command_Sound' )
commandManager.associate( 'window', 'Command_Window' )

print '******************************'
print '* PyJoke [LocalVersion V2.0] *'
print '******************************'

while not commandManager.exiting():
    command = raw_input( '#> ' )

    commandID = commandManager.put( command )
    print '[%s] Commande envoyé' % commandID

    commandManager.action()

    result = commandManager.get( commandID )
    print "[%s] <%d> %s" % ( commandID, result['CODE'], result['STATUS'] )

    for line in result['OUTPUT'].split( '\n' ):
        print '|> ', line
