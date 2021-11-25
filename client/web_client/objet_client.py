import requests as requ
from client.vue.session import Session
from client.web_client.dictoobjet import DicToObjet
from client.web_client.trad_web import TradWebconfig
from client.web_client.web_configuration import WebConfiguration
from objets_metier.caracteristique import Caracteristique
from objets_metier.joueur import Joueur
from objets_metier.monstre import Monstre
from objets_metier.objet import Objet
class ObjetClient():

    @staticmethod
    def ImportObjetWeb(index = str):
        url = str.format("{0}/{1}",'objet',index)
        index,desc = TradWebconfig.getTrad(url)
        return Objet(-1,index,desc)
    
    def ListeTypesObjet():
        return TradWebconfig.getTrad('objet')
    
    def ListeObjetsDeType(type):
        return 
    
    