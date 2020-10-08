import requests
import urllib.parse

def getID():
    daten1 = int(input("Day: "))
    daten2 = int(input("Month: "))
    daten3 = int(input("Year: "))
    params = {'daten1': daten1, 'daten2': daten2, 'daten3': daten3}
    params = urllib.parse.urlencode(params)
    r = requests.post('https://bv.ac-grenoble.fr/searchannu/src/infos_perso/etape2.php?login=%20')
    r = requests.get('https://bv.ac-grenoble.fr/searchannu/src/infos_perso/infos_perso.php?', params)
    txt = r.text
    a = "Informations" in txt
    if a:
        test="lol"
        file = open("links.txt", "a")
        file.write(params)
        file.write('\n')
        file.close()
        print("Utilisateur trouvé.")
        getID()
    else:
        print("Aucun utilisateur de ce nom.")
getID()
