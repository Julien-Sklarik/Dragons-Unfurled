from datetime import date
from typing import List

from client.exceptions.utilisateur_introuvable_exception import \
    UtilisateurIntrouvableException
from client.vue.session import Session
from client.web_client.feed_back_client import FeedBackClient
from objets_metier.feedback import FeedBack
from objets_metier.utilisateur import Utilisateur
from utils.singleton import Singleton
from web.dao.administrateur_dao import AdministrateurDAO
from web.dao.feed_back_dao import FeedBackDAO
from web.dao.joueur_dao import JoueurDAO
from web.dao.utilisateur_dao import UtilisateurDAO


class AdministrateurService(metaclass = Singleton):

    @staticmethod    
    def bannir(nom_utilisateur: str):
        if nom_utilisateur in JoueurDAO.liste_noms(): # Nous vérifions si ce nom d'utilisateur existe.
            AdministrateurDAO.supprimer_compte(nom_utilisateur)
        else:
            raise UtilisateurIntrouvableException(nom_utilisateur)

    @staticmethod
    def consulter_feed_back_admin():
        feed_backs = FeedBackClient.consulter_tous_les_feed_backs() 
        for ligne in feed_backs:
            info = dict(ligne)
            print(info["username"],"\n", FeedBack(id_feedback = info["id_feedback"], message = info["message"], date_ecriture = info["date_ecriture"]), "\n\n")


    @staticmethod
    def transferer_droits_admin(nom_utilisateur: str, nom_administrateur_donneur: str):
        if nom_utilisateur in JoueurDAO.liste_noms(): # Nous vérifions si ce nom d'utilisateur existe et n'est pas déjà administrateur.
            AdministrateurDAO.ajouter_droits_administrateur(nom_utilisateur)
            AdministrateurDAO.supprimer_droits_administrateur(nom_administrateur_donneur)
        else:
            raise UtilisateurIntrouvableException(nom_utilisateur)

    @staticmethod
    def repondre_feed_back(identifiant_joueur: str, message: str): # Cette fonction va effacer le feed-back et donner la réponse de l'administrateur.
        FeedBackDAO.donner_feedback(identifiant_joueur, FeedBack(id_feedback = -1, message = message, date_ecriture = date.today()))
