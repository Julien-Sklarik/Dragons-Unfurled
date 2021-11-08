from objets_metier.salle import Salle
from web.dao.salle_dao import SalleDAO
from web.dao.cellule_dao import CelluleDAO

class SalleService():

    @staticmethod
    def add_salle(id_donjon : int,  salle : Salle): 
        salle_persistee = SalleDAO.add_salle(id_donjon, salle)
        for i in range(salle.coordonnees_salle_cellule[0][0], salle.coordonnees_salle_cellule[1][0]):
            for j in range(salle.coordonnees_salle_cellule[0][1], salle.coordonnees_salle_cellule[1][1]):
                CelluleDAO.add_cellule(salle_persistee.id_salle, i, j)
            
