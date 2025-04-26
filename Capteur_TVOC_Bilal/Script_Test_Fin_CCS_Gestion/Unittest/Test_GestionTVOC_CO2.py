import unittest
from GestionTVOC_CO2 import GestionTVOC_CO2 

class TestGestionTVOC_CO2(unittest.TestCase):
    """ Tests unitaires pour la classe GestionTVOC_CO2 """

    def setUp(self):
        """ Initialisation avant chaque test """
        self.capteur = GestionTVOC_CO2()

    def test_initialisation_capteur(self):
        """ Vérifie que le capteur est bien initialisé """
        self.assertIsNotNone(self.capteur.capteur, "Le capteur ne devrait pas être None après initialisation.")

    def test_mesure_disponible(self):
        """ Vérifie si la récupération des mesures fonctionne correctement """
        co2, tvoc = self.capteur.get_mesure()
        self.assertTrue(co2 is None or (co2 >= 400 and co2 <= 5000), "Valeur de CO2 incohérente.")
        self.assertTrue(tvoc is None or (tvoc >= 0 and tvoc <= 1200), "Valeur de TVOC incohérente.")

if __name__ == "__main__":
    unittest.main()
