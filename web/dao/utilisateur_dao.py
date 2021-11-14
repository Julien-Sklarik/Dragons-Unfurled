from objets_metier.utilisateur import Utilisateur
from web.dao.db_connection import DBConnection
from client.exceptions.utilisateur_introuvable_exception import UtilisateurIntrouvableException
from psycopg2.extensions import register_adapter, AsIs
from pydantic import SecretBytes

# def adapt_pydantic_byte(Byte):
#         return AsIs(repr(Byte))

# register_adapter(SecretBytes, adapt_pydantic_byte)

class UtilisateurDAO:

    @staticmethod
    def liste_noms():
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT username "\
                    "FROM utilisateur"
                )
                res = cursor.fetchone()
        return []
        return res["username"]

    @staticmethod
    def verifie_mdp(utilisateur_nom: str, password: str) -> bool:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * "
                    "\nFROM utilisateur where utilisateur.utilisateur_nom=%(utilisateur_nom) and utilisateur.password=%(password)"
                )
                res = cursor.fetchone()
            if res["utilisateur_nom"] != None:
                return True
            return False

    @staticmethod
    def getUtilisateur(utilisateur_nom: str) -> Utilisateur:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * "\
                    "FROM Utilisateur where username=%(nom)s"\
                    ,{"nom" : utilisateur_nom}
                )
                res = cursor.fetchone()
        if res:
            return Utilisateur(connecte = True,
                                                mot_de_passe = res['password'],
                                                identifiant = res['username'],
                                                est_administrateur = False,
                                                feed_backs = True
                                                )
        else:
            raise UtilisateurIntrouvableException(utilisateur_nom)

    @staticmethod
    def createUtilisateur(utilisateur: Utilisateur) -> Utilisateur:
        try:
            UtilisateurDAO.getUtilisateur(utilisateur.identifiant)
        except UtilisateurIntrouvableException:
                with DBConnection().connection as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO Utilisateur (username, "\
                                                    "est_administrateur, "\
                                                    "password) "\
                            "VALUES "\
                            "(%(username)s,%(est_administrateur)s, %(password)s);", 
                            { "username" : utilisateur.identifiant
                            , "est_administrateur": utilisateur.est_administrateur
                            , "password": utilisateur.mot_de_passe}
                        )
                return utilisateur

    @staticmethod
    def updateUtilisateur(utilisateur_nom: str, utilisateur: Utilisateur) -> Utilisateur:
        utilisateur_to_update: Utilisateur = UtilisateurDAO.getUtilisateur(utilisateur_nom)
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE utilisateur SET utilisateur_nom=%(identifiant)s, password=%(password)s where id_utilisateur=%(id_utilisateur)s;", {"id_utilisateur": utilisateur_to_update.id, "utilisateur_nom": utilisateur.utilisateur_nom, "password": utilisateur.password})