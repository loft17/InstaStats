#!/usr/bin/env python3
# @author: Jose Luis Romera
# https://github.com/brunomb97/InstagramStats
# https://instaloader.github.io/
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog


import os, aux_funcs, argparse
import instaloader
import mysql.connector

from datetime import date

# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
today = date.today()
args = aux_funcs.get_args()


# Variables para conectar a Instagram
L = instaloader.Instaloader()
USER = args.user
PROFILE = USER

L.load_session_from_file(USER)
#profile = instaloader.Profile.from_username(L.context, PROFILE)

# Variables para colorear el texto en consola
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ------------------------------------------------------------------------------------------------------------------------
# Mostramos un menu de ayuda para ejecutar correctamente la aplicacion
def PrintUsage():
    #os.system('clear')    
    print("Usage: \n python3 main.py -u USERNAME -l LOGIN -o OPTIONS")
    print("\nOptions: ")
    print("\n- followers \t\t\t\t\tMostramos el numero total de cuentas que te siguen\n\t\t\t\t\t\ty el nombre de estas")
    print("\n- followees \t\t\t\t\tMostramos el numero total de cuentas que sigues\n\t\t\t\t\t\ty el nombre de estas")
    print("\n- nofollowback \t\t\t\t\tMostramos las cuentas que seguimos, pero estas\n\t\t\t\t\t\tno nos siguen a nosotros")
    print("\n- engagement \t\t\t\t\tMida el compromiso de Instagram y asegúrese de\n\t\t\t\t\t\tque su audiencia se mantenga conectada")
    #print("\n- ghostfollowers \t\t\t\tMe gusta de un perfil seguidores fantasmas\n\t\t\t\t\t\tPara obtener una lista de sus seguidores inactivos, es decir, seguidores a\n\t\t\t\t\t\tlos que no les gustó ninguna de sus imágenes, puede utilizar este enfoque.")
    print("\n- reporte \t\t\t\t\tGeneramos un reporte con los datos de nuestra cuenta")
    print("\n- ayuda / help \t\t\t\t\tMuestra las opciones disponibles")


# ------------------------------------------------------------------------------------------------------------------------
# conexión BBDD
ConnectBBDD=mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="pruebas",
	database="instagramstats")



# ------------------------------------------------------------------------------------------------------------------------
# Comprobamos que no exite un reporte anterior para no volver a generarlo
def ReportStatus():
    ConnectReportStatus=ConnectBBDD.cursor()
    ConnectReportStatus.execute(
        "SELECT status FROM reportstatus WHERE date = %s AND account = %s", (today, USER)
    )
    ConsultaSql = ConnectReportStatus.fetchone()  
    
    if(ConsultaSql == None):
        # Generamos el reporte
        ReportGenerate()
    else:
        # No hacemos nada
        PrintUsage


# --------------------------------------------------------------------------------------------------------------------------
# Comprobamos que no exite un reporte anterior para no volver a generarlo
# --------------------------------------------------------------------------------------------------------------------------
def ReportGenerate():
    profile = instaloader.Profile.from_username(L.context, PROFILE)

    # Conseguimos el Engagement actual y lo guardamos en la base de datos --------------------------------------------------
    num_followers = profile.followers
    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0

    for post in profile.get_posts():
        total_num_likes += post.likes
        total_num_comments += post.comments
        total_num_posts += 1

    # Formateamos el Engagement 
    engagement = float(total_num_likes + total_num_comments) / (num_followers * total_num_posts)
    os.system('clear')
    engagement=engagement * 100
    engagement = round(engagement, 2)  

    # Guardamos el dato del engadmet dentro de la BBDD
    ConnectEngagement=ConnectBBDD.cursor()
    datos=(today, USER, engagement)
    InsertEngagement="insert into engagement(date, account, engagement) values (%s,%s,%s)"
    ConnectEngagement.execute(InsertEngagement, datos)



    # Conseguimos los get_followees que nos siguien y la guardamos en la bbdd ----------------------------------------------
    ConnectFollowees=ConnectBBDD.cursor()
    followees = profile.get_followees()
   
    # Guardamos el dato del followers dentro de la BBDD
    InsertFollowees="insert into followees(date, followee, account) values (%s,%s,%s)"
    for followee in followees:
        datos=(today, followee.username, USER)
        ConnectFollowees.execute(InsertFollowees, datos)



    # Conseguimos los followers que nos siguien y la guardamos en la bbdd --------------------------------------------------
    ConnectFollowers=ConnectBBDD.cursor()
    followers = profile.get_followers()
   
    # Guardamos el dato del followers dentro de la BBDD
    InsertFollowers="insert into followers(date, follower, account) values (%s,%s,%s)"
    for follower in followers:
        datos=(today, follower.username, USER)
        ConnectFollowers.execute(InsertFollowers, datos)



    # Guardamos el registro en la base de datos de que se ha generado el reporte
    ConnectReportStatusW=ConnectBBDD.cursor()
    InsertReportStatusW="insert into reportstatus(date, account, status) values (%s,%s,%s)"
    datos=(today, USER, "1")
    ConnectReportStatusW.execute(InsertReportStatusW, datos)

    # Guardamos la BBDD y la cerramos --------------------------------------------------------------------------------------
    ConnectBBDD.commit()
    ConnectBBDD.close()



# --------------------------------------------------------------------------------------------------------------------------
# Mostrar los followers actuales desde la base de datos
# --------------------------------------------------------------------------------------------------------------------------
def ShowFollowersBBDD():
    TotalFollower = 0
    ConnectShowFollowers=ConnectBBDD.cursor()
    ConnectShowFollowers.execute(
        "SELECT follower FROM followers WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowFollowers = ConnectShowFollowers.fetchall()

    print(bcolors.OKGREEN + "\nFollowers:" + bcolors.ENDC)
    for AccountFriendships in SqlShowFollowers:
        TotalFollower=TotalFollower+1
        print(str(TotalFollower) + ". " + str(*AccountFriendships))



# --------------------------------------------------------------------------------------------------------------------------
# Mostrar los followers actuales desde la base de datos
# --------------------------------------------------------------------------------------------------------------------------
def ShowFolloweesBBDD():
    TotalFollowee = 0
    ConnectShowFollowees=ConnectBBDD.cursor()
    ConnectShowFollowees.execute(
        "SELECT followee FROM followees WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowFollowees = ConnectShowFollowees.fetchall()

    print(bcolors.OKGREEN + "\nFollowees:" + bcolors.ENDC)
    for AccountFriendships in SqlShowFollowees:
        TotalFollowee=TotalFollowee+1
        print(str(TotalFollowee) + ". " + str(*AccountFriendships))
       


# --------------------------------------------------------------------------------------------------------------------------
# Mostrar los que no nos siguen, pero nosotros si seguimos
# --------------------------------------------------------------------------------------------------------------------------
def NoFollowBackBBDD():
    TotalNoFollowBack = 0

    # Followers
    ConnectShowFollowers=ConnectBBDD.cursor()
    ConnectShowFollowers.execute(
        "SELECT follower FROM followers WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowFollowers = ConnectShowFollowers.fetchall()

    # Followings
    ConnectShowFollowees=ConnectBBDD.cursor()
    ConnectShowFollowees.execute(
        "SELECT followee FROM followees WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowFollowees = ConnectShowFollowees.fetchall()

    print(bcolors.OKGREEN + "\nNo Followback:" + bcolors.ENDC)
    for AccountNoFollowBack in SqlShowFollowees:
        if AccountNoFollowBack not in SqlShowFollowers:
            TotalNoFollowBack=TotalNoFollowBack+1
            print(str(TotalNoFollowBack) + ". " + str(*AccountNoFollowBack))



# --------------------------------------------------------------------------------------------------------------------------
# Mostrar el engadment actuales desde la base de datos
# --------------------------------------------------------------------------------------------------------------------------
def ShowEngagementBBDD():
    ConnectShowEngagement=ConnectBBDD.cursor()
    ConnectShowEngagement.execute(
        "SELECT engagement FROM engagement WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowEngagement = (str(*ConnectShowEngagement.fetchone()))
    print(bcolors.OKGREEN + "\nEngagement: " + bcolors.ENDC + SqlShowEngagement)



# --------------------------------------------------------------------------------------------------------------------------
# Mostrar el engadment historico, y su variacion con el dia anterior.
# --------------------------------------------------------------------------------------------------------------------------

# SELECT `date`, `account`, `engagement` FROM `engagement` WHERE `account` = 'lafustadeoro' 

def ShowEngagementHistoricoBBDD():
    ConnectShowEngagementHistorico=ConnectBBDD.cursor()
    ConnectShowEngagementHistorico.execute(
        "SELECT date, engagement FROM engagement WHERE account = %s", (USER, )
    )
    SqlShowEngagement = ConnectShowEngagementHistorico.fetchall()

    print(bcolors.OKGREEN + "\nFecha\t\t Engagement\t\t\t Diferencia" + bcolors.ENDC)
    for Engadment in SqlShowEngagement in range(2):
        print(Engadment[0], "\t", Engadment[1])




#------------------------------------------------------------------------------------------------------------------------
# Ejecucion
#------------------------------------------------------------------------------------------------------------------------
def main():
    ReportStatus()
    option = args.option

    if(option == "ayuda"):
        PrintUsage()
    
    elif(option == "reporte"):
        ReportGenerate()

    elif(option == "followers"):
        ShowFollowersBBDD()

    elif(option == "followees"):
        ShowFolloweesBBDD()

    elif(option == "engagement"):
        ShowEngagementBBDD()

    elif(option == "historicengagement"):
        ShowEngagementHistoricoBBDD()

    elif(option == "nofollowback"):
        NoFollowBackBBDD()

    elif(option == "test"):
        PrintUsage()

    elif(option == "help"):
        PrintUsage()

    else:
        PrintUsage()


if __name__ == "__main__":
		main()


