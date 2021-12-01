#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date
from configparser import ConfigParser

from scripts import nofollowback, showfollowees, showfollowers, medianumcomments, medianumlikes, totalnumfollowees, resumeninfoaccount, totalnumfollowers, showengagementBBDD, totalnumpost, totalnumcomments, totalnumlikes



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
# Mostrar los que no nos siguen, pero nosotros si seguimos
# ##########################################################################################################################
def NoFollowBack():
    TotalNoFollowBack = 0

    # Followers
    ConnectShowFollowers=ConnectBBDD.cursor()
    ConnectShowFollowers.execute(
        "SELECT followers FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    ListFollowers = list((str(*ConnectShowFollowers.fetchone())).split(" "))

    # Followees
    ConnectShowFollowees=ConnectBBDD.cursor()
    ConnectShowFollowees.execute(
        "SELECT followees FROM ig_report WHERE date = %s AND account = %s", (today, PROFILE)
    )
    ListFollowees = list((str(*ConnectShowFollowees.fetchone())).split(" "))

    print(color.OKGREEN + "No Followback:" + color.ENDC)
    for AccountNoFollowBack in ListFollowees:
        if AccountNoFollowBack not in ListFollowers:
            TotalNoFollowBack=TotalNoFollowBack+1
            print(str(TotalNoFollowBack) + ". " + str(AccountNoFollowBack))