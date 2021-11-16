from PyInquirer import Separator, prompt

from client.view.abstract_view import AbstractView
from client.view.session import Session
from client.view.maitre_du_jeu_view import MenuMJ
from client.view.joueur_view import MenuJoueur
from objets_metier.joueur import Joueur
from objets_metier.utilisateur import Utilisateur
from web.dao.campagne_dao import CampagneDAO
from web.dao.maitre_du_jeu_dao import MjDAO
from objets_metier.maitre_du_jeu import MaitreDuJeu

class AccueilJeuView(AbstractView):

    def __init__(self):
        utilisateur = Session.utilisateur 
        self.__questions = [
            {
                'type': 'list',
                'name': 'choix',
                'message': f'Bonjour {utilisateur.identifiant}, que souhaitez-vous faire ? ',
                'choices': [
                    'Rejoindre une campagne',
                    Separator(),
                    'Créer un personnage',
                    'Créer une campagne',
                    Separator(),
                    'Ecrire son feed-back',
                    'Consulter son feed-back',
                    'Se déconnecter',
                    
                ]
            }
        ]
    def display_info(self):
        with open('client/dessins_ascii/border.txt', 'r', encoding="utf-8") as affichage1, open('client/dessins_ascii/texte/accueil_de_jeu.txt', 'r', encoding="utf-8") as affichage2:
            print(affichage1.read(),affichage2.read())

    def make_choice(self):
        reponse = prompt(self.__questions)
        if reponse['choix'] == 'Créer un personnage':
            from client.view.creation_personnage_view import MenuPersonnage
            return MenuPersonnage()
            #faut ajouter la classe joueur pour le stocker je mets une val au pif pour l'instant
        
        if reponse['choix'] == 'Rejoindre une campagne': #Il faudrait charger une sauvegarde ici
            identifiant_campagne = input('Quel est l\'identifiant de votre campagne ?')
            if identifiant_campagne in CampagneDAO.liste_noms():
                campagne = CampagneDAO.get_campagne(identifiant_campagne) # liste avec l'id et le nom
                mj = CampagneDAO.trouve_mj(identifiant_campagne)
                liste_id_joueurs = mj.liste_joueurs()
                if self.utilisateur.identifiant in liste_id_joueurs:
                    if self.utilisateur.identifiant == mj.id_maitre_du_jeu:
                        personnage_joueur = mj.trouver_personnage(self.utilisateur) 
                        joueur = Joueur(personnage_joueur, self.utilisateur.connecte, self.utilisateur.mot_de_passe, self.utilisateur.identifiant, self.utilisateur.est_administrateur, self.utilisateur.feed_backs)
                        from client.view.maitre_du_jeu_view import MenuMJ
                        return MenuMJ(joueur, campagne)
                    else:
                        personnage_joueur = mj.trouver_personnage(self.utilisateur) 
                        personnages_joueurs = MjDAO.personnages_joueurs(campagne[0])
                        personnages_non_joueurs = MjDAO.personnages_non_joueurs(campagne[0])
                        monstres = MjDAO.monstres(campagne[0])
                        donjons = MjDAO.donjons(campagne[0])
                        maitre_du_jeu = MaitreDuJeu(campagne[0],campagne[1],personnage_joueur, self.utilisateur.connecte, self.utilisateur.mot_de_passe, self.utilisateur.identifiant, self.utilisateur.est_administrateur, self.utilisateur.feed_backs,personnages_joueurs,personnages_non_joueurs,monstres,donjons)
                        from client.view.joueur_view import MenuJoueur
                        return MenuJoueur(maitre_du_jeu,campagne)
                else:
                    print("Vous n'êtes pas membre de cette campagne.")
                    return AccueilJeuView()
            else:
                print("Cette campagne est introuvable.")
                return AccueilJeuView()

        if reponse['choix'] == 'Créer une campagne':
            nom_campagne = input("Ecrivez un nom pour votre campagne.")
            identifiant_campagne = CampagneDAO.creer_campagne(nom_campagne) #Creer_campagne affiche l'identifiant de la campagne
            return AccueilJeuView()
        
        if reponse['choix'] == 'Ecrire son feed-back':
            message = input("Écrivez le feed-back que vous souhaitez poster ?")
            Utilisateur.ecrire_son_feed_back(message)
            return AccueilJeuView()

        if reponse['choix'] == 'Consulter son feed-back':
            Utilisateur.consulter_son_feed_back()
            return AccueilJeuView()
        
        if reponse['choix'] == 'Se déconnecter':
            from client.view.deconnexion_view import Deconnexion
            return Deconnexion()