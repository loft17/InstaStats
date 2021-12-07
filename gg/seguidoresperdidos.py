#!/usr/bin/env python3
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date, timedelta
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


Lista1 = ["aaa", "bbb", "ccc", "ddd"]
Lista2 = ["aaa", "bbb", "ccc"]
Lista3 = ["aaa", "bbb", "ddd"]

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

#    for followee in Lista1:
#        if followee not in Lista2:
#            if followee not in Lista3:
#                print(followee)



# ##########################################################################################################################
# Numero TOTAL COMENTARIOS
# ##########################################################################################################################
def SeguidoresPerdidos():
    profile = instaloader.Profile.from_username(L.context, PROFILE)
    print("Seguidores perdidos:\n")

    x = 1
    DiaMenos = 1
    ListFollowersToday = []

    while (x >= 1):
        DateSearch = today - timedelta(DiaMenos)

        # Buscamos el registro mas actual que no sea de hoy.
        ConnectReportStatus=ConnectBBDD.cursor()
        ConnectReportStatus.execute(
            "SELECT date FROM ig_report WHERE date = %s AND account = %s", (DateSearch, PROFILE)
        )
        ConsultaSql = ConnectReportStatus.fetchone()


        if(ConsultaSql == None):
            DiaMenos = DiaMenos + 1
        else:
            # Sacamos los followers del registro mas actual que no sea de hoy.
            ConnectShowFollowers=ConnectBBDD.cursor()
            ConnectShowFollowers.execute(
                "SELECT followers FROM ig_report WHERE date = %s AND account = %s", (DateSearch, PROFILE)
            )
            ListFollowersOld = list((str(*ConnectShowFollowers.fetchone())).split(" "))

            # Sacamos los followers a dia de hoy
            followers = profile.get_followers()
            for follower in followers:
                ListFollowersToday.append(follower.username)

            for followee in ListFollowersOld:
                if followee not in ListFollowersToday:
                    print(followee)

            ## IMPORTANTE ## Terminamos el bucle
            break














