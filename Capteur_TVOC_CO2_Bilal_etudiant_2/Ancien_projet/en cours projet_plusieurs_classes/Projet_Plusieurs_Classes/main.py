from Capteur_TVOC_CO2 import CapteurTVOC_CO2

def main():
    """Programme principal pour lire les données du capteur CCS811."""
    capteur = CapteurTVOC_CO2()
    co2, tvoc = capteur.lire_mesure()
    if co2 is not None and tvoc is not None:
        print(f"CO2: {co2} ppm, TVOC: {tvoc} ppb")
    else:
        print("Erreur ou données non disponibles.")

if __name__ == "__main__":
    main()