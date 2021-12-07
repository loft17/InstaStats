import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser

from scripts import reportgenerate, detailslastpost, showtotalnum, medianum
from scripts import showfollowers, showfollowees


# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()
args = aux_funcs.get_args()

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")

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
# Resumen Info cuenta
# ##########################################################################################################################
def ResumenInfoAccount():
	print("\nInforme generado el", color.OKCYAN, today, color.ENDC)
	print("https://www.instagram.com/" + args.user)
	print("")
	
	showtotalnum.Post()
	showtotalnum.Likes()
	showtotalnum.Comments()
	showtotalnum.Followers()
	showtotalnum.Followers()
	medianum.Likes()
	medianum.Comments()
	showtotalnum.Engagement()

