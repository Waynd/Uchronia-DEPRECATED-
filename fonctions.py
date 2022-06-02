
def liste_var(liste):
    """
    Fonction qui permet de transformer une liste en variable, avec la mise en forme "habituelle" (avec les petits losanges bleus). Exemple d'utilisation:

    liste = ["Chameau", "Dromadaire", "Girafe"]
    variable_liste = liste_var(liste)
    print(variable_liste)

    >>> :small_blue_diamond: Chameau
            :small_blue_diamond: Dromadaire
            :small_blue_diamond: Girafe
    """
    x = ""
    for i in range(len(liste)):
        x = x + "\n :small_blue_diamond: " + liste[i]
    return x

##########

"""
Fonction qui...

"""

def fonction(x,y):
    pass

##########
