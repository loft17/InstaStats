#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

# TESTS
import sys
import fileinput


from datetime import date, timedelta
from configparser import ConfigParser

from scripts import version, menuayuda, nofollowback, showfollowees, showfollowers, medianumcomments
from scripts import medianumlikes, totalnumfollowees, resumeninfoaccount, totalnumfollowers
from scripts import showengagementBBDD, totalnumpost, totalnumcomments, totalnumlikes, ghostlastimg
from scripts import detailslastpost, seguidoresperdidos

# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()
args = aux_funcs.get_args()
statusvar = "0"

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")


# Variables para conectar a Instagram
L = instaloader.Instaloader()
#USER = args.user
#PROFILE = USER
USER = args.login
PROFILE = args.user




L.load_session_from_file(USER)
#profile = instaloader.Profile.from_username(L.context, PROFILE)

# Variables para colorear el texto en consola
color = printcolors.bcolors()

# ##########################################################################################################################
# conexión BBDD
# ##########################################################################################################################
ConnectBBDD=mysql.connector.connect(
	host =      (config.get('MYSQL', 'Server')),
	user =      (config.get('MYSQL', 'Username')),
	passwd =    (config.get('MYSQL', 'Password')),
	database =  (config.get('MYSQL', 'Database'))
)





















# ##########################################################################################################################
# Generamos un reporte para guardar en la base de datos
# ##########################################################################################################################
    #os.system('clear')
    #print("hola test")

def Test():
#    os.system('pwd')
#    with fileinput.FileInput("template_html2/index.html", inplace=True) as file:
#        for line in file:
#            print(line.replace(textToSearch, textToReplace), end='')


    # INDEX
     Var_TITLE_WEB= "{{ TITLE_WEB }}"
  



  






