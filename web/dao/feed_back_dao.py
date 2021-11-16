from objets_metier.feedback import FeedBack
from web.dao.db_connection import DBConnection
from objets_metier.utilisateur import Utilisateur
from client.view.session import Session

class FeedBackDAO:

    @staticmethod
    def donner_feedback(username : str, feed : FeedBack): 
        with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Feedback (message, "\
                                               "date_ecriture, "\
                                               "username ) "\

                        "VALUES "\
                        "(%(message)s,%(date_ecriture)s,%(username)s);", 
                        { "message" : feed.message
                        , "date_ecriture": feed.date_ecriture
                        , "username" : username}
                    )

    @staticmethod
    def consulter_tous():
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Feedback ")
                feed = cursor.fetchall()
        for ligne in feed:
            info = dict(ligne)
            print(FeedBack(info["id_feedback"], info["message"], info["date_ecriture"]) + "\n\n" )

    @staticmethod
    def consulter_feed_back():
        nom_utilisateur = Session.utilisateur.identifiant
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Feedback "\
                    "WHERE username = %(username)s;"
                    , {"username" : nom_utilisateur})
                feed = cursor.fetchall()
        for ligne in feed:
            info = dict(ligne)
            print(FeedBack(info["id_feedback"], info["message"], info["date_ecriture"]) + "\n\n" )