
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
statusvar = "0"

# Fichero de configuracion.
config = ConfigParser()
config.read("config.ini")


# Variables para conectar a Instagram
#L = instaloader.Instaloader()
#USER = args.login
#PROFILE = args.user





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
def ReportGenerate():
    # Conexion Instagram
    L = instaloader.Instaloader()
    L.load_session_from_file(args.login)
    profile = instaloader.Profile.from_username(L.context, args.user)

    # ----------------------------------------------------------------------------------------------------------------------
    # Variables a 0
    # ----------------------------------------------------------------------------------------------------------------------    
    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    total_num_followers = 0
    total_num_followees = 0
    listado_followees = []
    listado_followers = []
    listado_unfollowers = []



    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos el Engagement, likes, coments, post actual y lo guardamos en la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    num_followers = profile.followers
    for post in profile.get_posts():
        total_num_likes += post.likes
        total_num_comments += post.comments
        total_num_posts += 1

    engagement = round((float(total_num_likes + total_num_comments) / (num_followers * total_num_posts) * 100), 2)
    #print(engagement)
    


    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos los get_followees que nos siguien
    # ----------------------------------------------------------------------------------------------------------------------
    followees = profile.get_followees()
    for followee in followees:
        total_num_followees=total_num_followees+1
        listado_followees.append(followee.username)
        #print(followee.username)

    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos los get_followers que nos siguien
    # ----------------------------------------------------------------------------------------------------------------------
    followers = profile.get_followers()
    for follower in followers:
        total_num_followers=total_num_followers+1
        listado_followers.append(follower.username)
        #print(follower.username)


    # ----------------------------------------------------------------------------------------------------------------------
    # Conseguimos los unfollowers
    # ----------------------------------------------------------------------------------------------------------------------
    x = 1
    DiaMenos = 1
    ListFollowersToday = []

    while (x >= 1):
        DateSearch = today - timedelta(DiaMenos)

        # Buscamos el registro mas actual que no sea de hoy.
        ConnectReportStatus=ConnectBBDD.cursor()
        ConnectReportStatus.execute(
            "SELECT date FROM ig_report WHERE date = %s AND account = %s", (DateSearch, args.user)
        )
        ConsultaSql = ConnectReportStatus.fetchone()


        if(ConsultaSql == None):
            DiaMenos = DiaMenos + 1
        else:
            # Sacamos los followers del registro mas actual que no sea de hoy.
            ConnectShowFollowers=ConnectBBDD.cursor()
            ConnectShowFollowers.execute(
                "SELECT followers FROM ig_report WHERE date = %s AND account = %s", (DateSearch, args.user)
            )
            ListFollowersOld = list((str(*ConnectShowFollowers.fetchone())).split(" "))

            # Sacamos los followers a dia de hoy
            followers = profile.get_followers()
            for follower in followers:
                ListFollowersToday.append(follower.username)

            for unfollower in ListFollowersOld:
                if unfollower not in ListFollowersToday:
                    listado_unfollowers.append(follower.username)

            ## IMPORTANTE ## Terminamos el bucle
            break




    # ----------------------------------------------------------------------------------------------------------------------
    # Convertimos la lista en STR y eliminamos caracteres innecesarios para la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    characters = ",'[]"
    srt_followees = str(listado_followees)
    srt_followers = str(listado_followers)
    srt_unfollowers = str(listado_unfollowers)

    for x in range(len(characters)):
        srt_followees = srt_followees.replace(characters[x],"")
        srt_followers = srt_followers.replace(characters[x],"")
        srt_unfollowers = srt_unfollowers.replace(characters[x],"")



    # ----------------------------------------------------------------------------------------------------------------------
    # Sacamos el ID del usuario
    # ----------------------------------------------------------------------------------------------------------------------
    userid_account = re.sub('[^A-Za-z0-9]+', '', (str(profile).split("(", 1)[1]))



    # ----------------------------------------------------------------------------------------------------------------------
    # Guardamos toda la informacion en la base de datos
    # ----------------------------------------------------------------------------------------------------------------------
    ConnectInfo=ConnectBBDD.cursor()
    InsertInfo="insert into ig_report(date, account, userid, followers, followees, unfollowers, count_followers, count_followees, total_likes, total_comments, total_post, engagement) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    datos=(today, args.user, userid_account, srt_followers, srt_followees, srt_unfollowers, total_num_followers, total_num_followees, total_num_likes, total_num_comments, total_num_posts, engagement)
    ConnectInfo.execute(InsertInfo, datos)
    
   
    # Guardamos la BBDD y la cerramos --------------------------------------------------------------------------------------
    ConnectBBDD.commit()










