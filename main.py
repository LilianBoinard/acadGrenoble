import requests
import urllib.parse
from termcolor import colored, cprint
from bs4 import BeautifulSoup as bs
import sys


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
    choice = input("Mode pilote automatique ? (y/n)\n")
    if choice == "y":
        automatic()
    elif choice == "n":
        withInput()
        process()
    else:
        print('Vous devez entrer "y" (oui) ou "n" (non)')
        getID()
    
getID()
