import requests as requ
from client.vue.session import Session
from client.web_client.dictoobjet import DicToObjet
from client.web_client.trad_web import TradWebconfig
from client.web_client.web_configuration import WebConfiguration
from objets_metier.caracteristique import Caracteristique
from objets_metier.joueur import Joueur
from objets_metier.monstre import Monstre

class MonstreClient():
    
        @staticmethod
        def ImportMonstreWeb(nom = str):
            Session.utilisateur = Joueur(identifiant = 'jules')
            util = Session.utilisateur
            configuration = TradWebconfig()
            d = configuration.getTrad('monstre/' + nom)
            MonstreClient.FormatMonstre(d)
            carac = DicToObjet.dictocarac(d)
            return Monstre(util.identifiant,-1,d['type'],carac)
            
    
        @staticmethod
        def ImportMonstreParType(triche = bool):
            pass
        
        @staticmethod
        def ImportListeTypes():
            pass
            
        @staticmethod
        def FormatMonstre(dic):
            #On part du principe que le dictionnaire contient des attaques et des capacites, et le but ici est de les formater pour les afficher
            #C'est sur place par simplicité, et on y ajoute les actions légendaires
            listattaques = []
            listcapacites = []
            list = dic['attaques']
            list2 = dic['capacites']
            list3 = dic['attaques_legendaires']
            for dico in list :
                listattaques.append(dico['name']) 
            for dico2 in list2 : 
                listcapacites.append(dico2['name'])
            for dico3 in list3 : 
                listattaques.append(dico3['name']+'(legendaire)')
            dic.update({'attaques' : listattaques})
            dic.update({'capacites' : listcapacites})
            
        