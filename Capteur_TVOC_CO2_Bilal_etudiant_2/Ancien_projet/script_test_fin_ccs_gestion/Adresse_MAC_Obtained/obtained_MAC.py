from getmac import get_mac_address


def main():
    """Affiche l'adresse MAC formatée de l'interface wlan0."""
    mac = get_mac_address(interface="wlan0")
    if mac is not None:
        formatted_mac = mac.replace(":", "")
        print("L'adresse MAC est :", formatted_mac)
    else:
        print("Impossible de récupérer l'adresse MAC.")


if __name__ == "__main__":
    main()