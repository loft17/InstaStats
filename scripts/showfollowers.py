import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date, timedelta
from configparser import ConfigParser

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
# Mostrar los followers actuales desde la base de datos
# ##########################################################################################################################
def ShowFollowers():
    TotalFollower = 0
    ConnectShowFollowers=ConnectBBDD.cursor()
    ConnectShowFollowers.execute(
        "SELECT followers FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    ListFollowers = list((str(*ConnectShowFollowers.fetchone())).split(" "))
    print(ListFollowers)

    print(color.OKGREEN + "\nFollowers:" + color.ENDC)
    for AccountFriendships in ListFollowers:
        TotalFollower=TotalFollower+1
        print(str(TotalFollower) + ". " + AccountFriendships)