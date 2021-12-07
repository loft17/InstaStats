# ------------------------------------------------------------------------------------------------------------------------
# Mostramos un menu de ayuda para ejecutar correctamente la aplicacion
# ------------------------------------------------------------------------------------------------------------------------
def PrintUsage():
    #os.system('clear')    
    print("Usage: \n python3 main.py -u USERNAME -l LOGIN -o OPTIONS")
    print("\nOptions: ")
    
    print("\n- reporte \t\t\t\t\tGeneramos un reporte con los datos de nuestra cuenta")
    print("\n- resumeninfo \t\t\t\t\tMuestra un resumen general de la cuenta")
    print("\n- detailslastpost \t\t\t\tMuestra un resumen general de las ultimas imagenes")

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

    print("\n- ghostlastimgfollowees\t\t\t\tMuestra a quien sigues que no han dado like en tus ultimas\n\t\t\t\t\t\t20 imagenes")
    print("\n- ghostlastimgfollowers\t\t\t\tMuestra tus seguidores que no han dado like en tus ultimas\n\t\t\t\t\t\t20 imagenes")
    print("\n- ghosttotalimgfollowees\t\t\tMuestra tus seguidores que no han dado like en ninguna de tus\n\t\t\t\t\t\timagenes")
    print("\n- ghosttotalimgfollowers\t\t\tMuestra a quien sigues que no han dado like en ninguna de tus\n\t\t\t\t\t\timagenes")

    print("\n- seguidoresperdidos\t\t\tMuestra tus seguidores peridos")


    print("\n- version\t\t\t\t\tMuestra la version del programa")
    print("\n- ayuda / help \t\t\t\t\tMuestra las opciones disponibles")