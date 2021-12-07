import os, aux_funcs, argparse, re, printcolors
import instaloader
import mysql.connector

from datetime import date, datetime
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
# Mostrar los que no nos siguen, pero nosotros si seguimos
# ##########################################################################################################################
def NoFollowBack():
    TotalNoFollowBack = 0

    # Followers
    ConnectShowFollowers=ConnectBBDD.cursor()
    ConnectShowFollowers.execute(
        "SELECT followers FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    ListFollowers = list((str(*ConnectShowFollowers.fetchone())).split(" "))

    # Followees
    ConnectShowFollowees=ConnectBBDD.cursor()
    ConnectShowFollowees.execute(
        "SELECT followees FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    ListFollowees = list((str(*ConnectShowFollowees.fetchone())).split(" "))

    print(color.OKGREEN + "\nNo Followback:" + color.ENDC)
    for AccountNoFollowBack in ListFollowees:
        if AccountNoFollowBack not in ListFollowers:
            TotalNoFollowBack=TotalNoFollowBack+1
            print(str(TotalNoFollowBack) + ". " + str(AccountNoFollowBack))




# ##########################################################################################################################
# Mostrar los que no nos siguen, pero nosotros si seguimos
# ##########################################################################################################################
def NoFollowBackExt():
    TotalNoFollowBack = 0

    # Followers
    ConnectShowFollowers=ConnectBBDD.cursor()
    ConnectShowFollowers.execute(
        "SELECT followers FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    ListFollowers = list((str(*ConnectShowFollowers.fetchone())).split(" "))

    # Followees
    ConnectShowFollowees=ConnectBBDD.cursor()
    ConnectShowFollowees.execute(
        "SELECT followees FROM ig_report WHERE date = %s AND account = %s", (today, args.user)
    )
    ListFollowees = list((str(*ConnectShowFollowees.fetchone())).split(" "))

    print(color.OKGREEN + "\n   Follower\t\t  Ultima imagen" + color.ENDC)
    for AccountNoFollowBack in ListFollowees:
        if AccountNoFollowBack not in ListFollowers:
            TotalNoFollowBack=TotalNoFollowBack+1

            # Sacamos la info de la cuenta que no nos sigue
            L = instaloader.Instaloader()
            L.load_session_from_file(args.login)
            #profile = instaloader.Profile.from_username(L.context, args.user)
            profile = instaloader.Profile.from_username(L.context, str(AccountNoFollowBack))

            NumImange = 0

            for post in profile.get_posts():
                if(NumImange == 1):
                    break
                else:
                    # Añadimos 1 al contador de imagenes
                    NumImange = NumImange + 1
                    #print(datetime.strptime(str(post.date_utc), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"))
                    print(str(TotalNoFollowBack) + ". " + str(AccountNoFollowBack), "\t\t", datetime.strptime(str(post.date_utc), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y"))


    


            # print(str(TotalNoFollowBack) + ". " + str(AccountNoFollowBack))