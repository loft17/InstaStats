#!/usr/bin/env python3
# @author: Jose Luis Romera
# https://github.com/brunomb97/InstagramStats
# https://instaloader.github.io/
# python3 InstaStats.py kojiro_thedog --login kojiro_thedog

import os, aux_funcs, argparse, re
import instaloader
import mysql.connector

from datetime import date

### EJEMPLO https://www.followerstat.com/report/emrata
#https://oinkmygod.com/blog/herramientas-analitica-instagram/
## Average Values of this Instagram Profile
# Engagement Rate **
# Average Likes
# Average Likes
# Average Comments
# Comment Rate
# Average Cost per post
# Posts por semana
# Posts por mes
# Posts por año
# Followers por post
# Seguidores perdidos
# Seguidores ganados
# 
## Account Stats Summary
# Date -- Followers -- dif -- Following -- dif -- Uploads -- dif
# 
#El porcentaje de seguidores que vas ganando a lo largo del tiempo. 
#Para calcularlo, simplemente tienes que dividir el número de seguidores
#que has conseguido en un plazo de tiempo (por ejemplo, en el último mes)
#entre el número de seguidores que tenías al inicio del plazo del tiempo
#(hace justo un mes) y multiplicarlo por 100.

# ------------------------------------------------------------------------------------------------------------------------
# Variales
# ------------------------------------------------------------------------------------------------------------------------
VersionApp = "0.0.1 (November 24, 2021)"
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
# ------------------------------------------------------------------------------------------------------------------------
def PrintUsage():
    #os.system('clear')    
    print("Usage: \n python3 main.py -u USERNAME -l LOGIN -o OPTIONS")
    print("\nOptions: ")
    print("\n- reporte \t\t\t\t\tGeneramos un reporte con los datos de nuestra cuenta")
    print("\n- resumeninfo \t\t\t\t\tMuestra un resumen general de la cuenta")
    print("\n- followers \t\t\t\t\tMuestra las de cuentas que te siguen y el nombre de estas")
    print("\n- followees \t\t\t\t\tMuestra las  cuentas que sigues y el nombre de estas")
    print("\n- nofollowback \t\t\t\t\tMostramos las cuentas que seguimos, pero estas no\n\t\t\t\t\t\tnos siguen a nosotros")
    print("\n- engagement \t\t\t\t\tSe trata del porcentaje de tus seguidores que interactúa con\n\t\t\t\t\t\ttus publicaciones. La media de interacciones que tu cuenta\n\t\t\t\t\t\tconsigue en general. ")
    #print("\n- ghostfollowers \t\t\t\tMe gusta de un perfil seguidores fantasmas\n\t\t\t\t\t\tPara obtener una lista de sus seguidores inactivos, es decir, seguidores a\n\t\t\t\t\t\tlos que no les gustó ninguna de sus imágenes, puede utilizar este enfoque.")

    print("\n- numtotallikes\t\t\t\t\tMuestra el numero total de likes recibidos")
    print("\n- numtotalcomments\t\t\t\tMuestra el numero total de comentarios recibidos")
    print("\n- numtotalposts\t\t\t\t\tMuestra el numero total de posts recibidos")
    print("\n- numtotalfollowers\t\t\t\tMuestra el numero total de followers recibidos")
    print("\n- numtotalfollowees\t\t\t\tMuestra el numero total de followees recibidos")
    print("\n- medialikes\t\t\t\t\tMuestra la media de likes recibidos entre los posts")
    print("\n- mediacomentarios\t\t\t\tMuestra la media de comentarios recibidos entre los posts")

    print("\n- version\t\t\t\t\tMuestra la version del programa")
    print("\n- ayuda / help \t\t\t\t\tMuestra las opciones disponibles")



# ------------------------------------------------------------------------------------------------------------------------
# conexión BBDD
# ------------------------------------------------------------------------------------------------------------------------
ConnectBBDD=mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="pruebas",
	database="instagramstats")



# ------------------------------------------------------------------------------------------------------------------------
# VERSION
# ------------------------------------------------------------------------------------------------------------------------
def versionapp():
    print("Version del programa:", VersionApp)

# ------------------------------------------------------------------------------------------------------------------------
# Comprobamos que no exite un reporte anterior para no volver a generarlo
# ------------------------------------------------------------------------------------------------------------------------
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

    # Conseguimos el Engagement, likes, coments, post actual y lo guardamos en la base de datos ----------------------------
    num_followers = profile.followers
    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    total_num_followers = 0
    total_num_followees = 0

    for post in profile.get_posts():
        total_num_likes += post.likes
        total_num_comments += post.comments
        total_num_posts += 1

    # Formateamos el Engagement 
    engagement = float(total_num_likes + total_num_comments) / (num_followers * total_num_posts)
    engagement=engagement * 100
    engagement = round(engagement, 2)

    # Conseguimos los get_followees que nos siguien y la guardamos en la bbdd ----------------------------------------------
    ConnectFollowees=ConnectBBDD.cursor()
    followees = profile.get_followees()
   
    # Guardamos el dato del followers dentro de la BBDD
    InsertFollowees="insert into followees(date, followee, account) values (%s,%s,%s)"
    for followee in followees:
        total_num_followees=total_num_followees+1
        datos=(today, followee.username, USER)
        ConnectFollowees.execute(InsertFollowees, datos)

    # Conseguimos los followers que nos siguien y la guardamos en la bbdd --------------------------------------------------
    ConnectFollowers=ConnectBBDD.cursor()
    followers = profile.get_followers()
   
    # Guardamos el dato del followers dentro de la BBDD
    InsertFollowers="insert into followers(date, follower, account) values (%s,%s,%s)"
    for follower in followers:
        total_num_followers=total_num_followers+1
        datos=(today, follower.username, USER)
        ConnectFollowers.execute(InsertFollowers, datos)

    # Sacamos el ID del usuario
    userid_account = re.sub('[^A-Za-z0-9]+', '', (str(profile).split("(", 1)[1]))

    # Guardamos el dato del engadmet dentro de la BBDD
    ConnectInfo=ConnectBBDD.cursor()
    InsertInfo="insert into generalinfo(date, account, userid_account, followers, followees, total_likes, total_comments, total_post, engagement) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    datos=(today, USER, userid_account, total_num_followers, total_num_followees, total_num_likes, total_num_comments, total_num_posts, engagement)
    ConnectInfo.execute(InsertInfo, datos)

    # Guardamos el registro en la base de datos de que se ha generado el reporte
    ConnectReportStatusW=ConnectBBDD.cursor()
    InsertReportStatusW="insert into reportstatus(date, account, status) values (%s,%s,%s)"
    datos=(today, USER, "1")
    ConnectReportStatusW.execute(InsertReportStatusW, datos)

    # Guardamos la BBDD y la cerramos --------------------------------------------------------------------------------------
    ConnectBBDD.commit()
    #ConnectBBDD.close()




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
        "SELECT engagement FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowEngagement = (str(*ConnectShowEngagement.fetchone()))
    print("Engagement: " + bcolors.OKGREEN + SqlShowEngagement + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Mostrar el engadment historico, y su variacion con el dia anterior.
# --------------------------------------------------------------------------------------------------------------------------
def ShowEngagementHistoricoBBDD():
    ConnectShowEngagementHistorico=ConnectBBDD.cursor()
    ConnectShowEngagementHistorico.execute(
        "SELECT date, engagement FROM engagement WHERE account = %s", (USER, )
    )
    SqlShowEngagement = ConnectShowEngagementHistorico.fetchall()

    print(bcolors.OKGREEN + "\nFecha\t\t Engagement\t\t\t Diferencia" + bcolors.ENDC)
    for Engadment in SqlShowEngagement:
        print(Engadment[0], "\t", Engadment[1])


# --------------------------------------------------------------------------------------------------------------------------
# Numero TOTAL LIKES
# --------------------------------------------------------------------------------------------------------------------------
def TotalNumLikes():
    ConnectShowTotalLikes=ConnectBBDD.cursor()
    ConnectShowTotalLikes.execute(
        "SELECT total_likes FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowTotalNumLikes = (str(*ConnectShowTotalLikes.fetchone()))
    print("Total Likes: " + bcolors.OKGREEN + SqlShowTotalNumLikes + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero MEDIA LIKES por post
# --------------------------------------------------------------------------------------------------------------------------
def MediaNumLikes():
    ConnectShowMediaLikes=ConnectBBDD.cursor()
    ConnectShowMediaLikes.execute(
        "SELECT total_likes FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowMediaNumLikes = (int(*ConnectShowMediaLikes.fetchone()))
    
    ConnectShowMediaLikes.execute(
        "SELECT total_post FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowMediaNumPost = (int(*ConnectShowMediaLikes.fetchone()))

    NumMediaLikesPosts = round(SqlShowMediaNumLikes / SqlShowMediaNumPost, 2)
    print("Media Likes por post: " + bcolors.OKGREEN + str(NumMediaLikesPosts) + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero MEDIA COMENTARIOS por post
# --------------------------------------------------------------------------------------------------------------------------
def MediaNumComments():
    ConnectShowMediaComments=ConnectBBDD.cursor()
    ConnectShowMediaComments.execute(
        "SELECT total_comments FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowMediaNumComments = (int(*ConnectShowMediaComments.fetchone()))
    
    ConnectShowMediaComments.execute(
        "SELECT total_post FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowMediaNumPost = (int(*ConnectShowMediaComments.fetchone()))

    NumMediaCommentsPosts = round(SqlShowMediaNumComments / SqlShowMediaNumPost, 2)
    print("Media comentarios por post: " + bcolors.OKGREEN + str(NumMediaCommentsPosts) + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero TOTAL Posts
# --------------------------------------------------------------------------------------------------------------------------
def TotalNumPosts():
    ConnectShowTotalPosts=ConnectBBDD.cursor()
    ConnectShowTotalPosts.execute(
        "SELECT total_post FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowTotalNumPosts = (str(*ConnectShowTotalPosts.fetchone()))
    print("Total Posts: " + bcolors.OKGREEN + SqlShowTotalNumPosts + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero TOTAL Comments
# --------------------------------------------------------------------------------------------------------------------------
def TotalNumComments():
    ConnectShowTotalComments=ConnectBBDD.cursor()
    ConnectShowTotalComments.execute(
        "SELECT total_comments FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowTotalNumComments = (str(*ConnectShowTotalComments.fetchone()))
    print("Total Comentarios: " + bcolors.OKGREEN + SqlShowTotalNumComments + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero TOTAL Posts
# --------------------------------------------------------------------------------------------------------------------------
def TotalNumPosts():
    ConnectShowTotalPosts=ConnectBBDD.cursor()
    ConnectShowTotalPosts.execute(
        "SELECT total_post FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowTotalNumPosts = (str(*ConnectShowTotalPosts.fetchone()))
    print("Total Posts: " + bcolors.OKGREEN + SqlShowTotalNumPosts + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero TOTAL Followers
# --------------------------------------------------------------------------------------------------------------------------
def TotalNumFollowers():
    ConnectShowTotalFollowers=ConnectBBDD.cursor()
    ConnectShowTotalFollowers.execute(
        "SELECT followers FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowTotalNumFollowers = (str(*ConnectShowTotalFollowers.fetchone()))
    print("Total Followers: " + bcolors.OKGREEN + SqlShowTotalNumFollowers + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Numero TOTAL Followers
# --------------------------------------------------------------------------------------------------------------------------
def TotalNumFollowees():
    ConnectShowTotalFollowees=ConnectBBDD.cursor()
    ConnectShowTotalFollowees.execute(
        "SELECT followees FROM generalinfo WHERE date = %s AND account = %s", (today, USER)
    )
    SqlShowTotalNumFollowees = (str(*ConnectShowTotalFollowees.fetchone()))
    print("Total Followees: " + bcolors.OKGREEN + SqlShowTotalNumFollowees + bcolors.ENDC)



# --------------------------------------------------------------------------------------------------------------------------
# Resumen Info cuenta
# --------------------------------------------------------------------------------------------------------------------------
def ResumenInfoAccount():
    print("\nInforme generado el", bcolors.OKCYAN, today, bcolors.ENDC)
    print("url: https://www.instagram.com/" + USER)
    print("")
    TotalNumFollowers()
    TotalNumFollowees()
    TotalNumLikes()
    TotalNumComments()
    TotalNumPosts()
    ShowEngagementBBDD()
    MediaNumLikes()
    MediaNumComments()
    print("")



def test():
#    profile = instaloader.Profile.from_username(L.context, PROFILE)

    #profile = "<Profile lafustadeoro (7538016399)>"
    #profile = (str(profile))
    #profile = (profile.split("(", 1)[1])
    #profile = (profile[1])
#    test = re.sub('[^A-Za-z0-9]+', '', (str(profile).split("(", 1)[1]))
    print("aa")

  
    
    
    
    
    
 


#------------------------------------------------------------------------------------------------------------------------
# Ejecucion
#------------------------------------------------------------------------------------------------------------------------
def main():
    ReportStatus()
    option = args.option

    if(option == "ayuda"):
        PrintUsage()
    
    elif(option == "reporte"):
        ReportStatus()

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

    elif(option == "numtotallikes"):
        TotalNumLikes()

    elif(option == "numtotalcomments"):
        TotalNumComments()

    elif(option == "numtotalposts"):
        TotalNumPosts()

    elif(option == "numtotalfollowers"):
        TotalNumFollowers()

    elif(option == "numtotalfollowees"):
        TotalNumFollowees()

    elif(option == "numtotalfollowees"):
        TotalNumFollowees()

    elif(option == "medialikes"):
        MediaNumLikes()

    elif(option == "mediacomentarios"):
        MediaNumComments()

    elif(option == "resumeninfo"):
        ResumenInfoAccount()

    elif(option == "test"):
        test()

    elif(option == "version"):
        versionapp()

    elif(option == "help"):
        PrintUsage()

    else:
        PrintUsage()

    # Cerramos la base de datos antes de que se cierre la aplicacion
    ConnectBBDD.close()

if __name__ == "__main__":
		main()
        