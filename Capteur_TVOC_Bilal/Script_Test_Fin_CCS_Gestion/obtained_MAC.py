from getmac import get_mac_address

win_mac = get_mac_address(interface="wlan0")

# Pour supprimer les : car par défaut il le donne. 
formatted_mac = win_mac.replace(":", "")

print("L'adresse MAC est  : ", formatted_mac)