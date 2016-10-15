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

print '******************************'
print '* PyJoke [LocalVersion V2.0] *'
print '******************************'

while not commandManager._ENV_['EXITING']:
    command = raw_input( '#> ' )

    commandID = commandManager.send( command )
    print '[%s] Commande envoyé' % commandID

    commandManager.action()

    result = commandManager.get( commandID )
    print "[%s] <%d> %s" % ( commandID, result['CODE'], result['STATUS'] )

    for line in result['OUTPUT'].split( '\n' ):
        print '|> ', line
