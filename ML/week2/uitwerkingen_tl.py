import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

# ==== OPGAVE 1 ====
def plotNumber(nrVector):
    # Let op: de manier waarop de data is opgesteld vereist dat je gebruik maakt
    # van de Fortran index-volgorde – de eerste index verandert het snelst, de 
    # laatste index het langzaamst; als je dat niet doet, wordt het plaatje 
    # gespiegeld en geroteerd. Zie de documentatie op 
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html

    matrix = np.reshape(nrVector, (20, 20), 'F')
    plt.matshow(matrix)
    plt.show()

# ==== OPGAVE 2a ====
def sigmoid(z):
    # Maak de code die de sigmoid van de input z teruggeeft. Zorg er hierbij
    # voor dat de code zowel werkt wanneer z een getal is als wanneer z een
    # vector is.
    # Maak gebruik van de methode exp() in NumPy.

    sigmoid = 1 / (1 + np.exp(-z))
    return sigmoid

# ==== OPGAVE 2b ====
def get_y_matrix(y, m):
    # Gegeven een vector met waarden y_i van 1...x, retourneer een (ijle) matrix
    # van m×x met een 1 op positie y_i en een 0 op de overige posities.
    # Let op: de gegeven vector y is 1-based en de gevraagde matrix is 0-based,
    # dus als y_i=1, dan moet regel i in de matrix [1,0,0, ... 0] zijn, als
    # y_i=10, dan is regel i in de matrix [0,0,...1] (in dit geval is de breedte
    # van de matrix 10 (0-9), maar de methode moet werken voor elke waarde van 
    # y en m

    cols = [i[0] for i in y-1]
    rows = [i for i in range(len(cols))]
    data = [1 for _ in range(len(rows))]
    y_matrix = csr_matrix((data, (rows, cols))).toarray()
    return y_matrix

# ==== OPGAVE 2c ==== 
# ===== deel 1: =====
def predictNumber(Theta1, Theta2, X):
    # Deze methode moet een matrix teruggeven met de output van het netwerk
    # gegeven de waarden van Theta1 en Theta2. Elke regel in deze matrix 
    # is de waarschijnlijkheid dat het sample op die positie (i) het getal
    # is dat met de kolom correspondeert.

    # De matrices Theta1 en Theta2 corresponderen met het gewicht tussen de
    # input-laag en de verborgen laag, en tussen de verborgen laag en de
    # output-laag, respectievelijk. 

    # Een mogelijk stappenplan kan zijn:

    #    1. voeg enen toe aan de gegeven matrix X; dit is de input-matrix a1
    #    2. roep de sigmoid-functie van hierboven aan met a1 als actuele
    #       parameter: dit is de variabele a2
    #    3. voeg enen toe aan de matrix a2, dit is de input voor de laatste
    #       laag in het netwerk
    #    4. roep de sigmoid-functie aan op deze a2; dit is het uiteindelijke
    #       resultaat: de output van het netwerk aan de buitenste laag.

    # Voeg enen toe aan het begin van elke stap en reshape de uiteindelijke
    # vector zodat deze dezelfde dimensionaliteit heeft als y in de exercise.

    m, n = X.shape
    a1 = np.c_[np.ones(m), X]
    z2 = np.dot(a1, Theta1.T)
    a2 = sigmoid(z2)
    a2 = np.c_[np.ones(m), a2]
    z3 = np.dot(a2, Theta2.T)
    a3 = sigmoid(z3)

    return a3

# ===== deel 2: =====
def computeCost(Theta1, Theta2, X, y):
    # Deze methode maakt gebruik van de methode predictNumber() die je hierboven hebt
    # geïmplementeerd. Hier wordt het voorspelde getal vergeleken met de werkelijk 
    # waarde (die in de parameter y is meegegeven) en wordt de totale kost van deze
    # voorspelling (dus met de huidige waarden van Theta1 en Theta2) berekend en
    # geretourneerd.
    # Let op: de y die hier binnenkomt is de m×1-vector met waarden van 1...10. 
    # Maak gebruik van de methode get_y_matrix() die je in opgave 2a hebt gemaakt
    # om deze om te zetten naar een matrix. 

    k = predictNumber(Theta1, Theta2, X) # Voorspelling
    y = get_y_matrix(y, y.shape[0])      # Correcte waarden

    m, n = X.shape
    cost = 1 / m * np.sum(np.multiply(np.log(k), -y) - np.multiply(np.log(1 - k), (1 - y)))

    return cost
    # https://datascience.stackexchange.com/questions/22470/python-implementation-of-cost-function-in-logistic-regression-why-dot-multiplic\

# ==== OPGAVE 3a ====
def sigmoidGradient(z): 
    # Retourneer hier de waarde van de afgeleide van de sigmoïdefunctie.
    # Zie de opgave voor de exacte formule. Zorg ervoor dat deze werkt met
    # scalaire waarden en met vectoren.

    g = sigmoid(z)
    return g * (1 - g)

# ==== OPGAVE 3b ====
def nnCheckGradients(Theta1, Theta2, X, y):
    # Retourneer de gradiënten van Theta1 en Theta2, gegeven de waarden van X en van y
    # Zie het stappenplan in de opgaven voor een mogelijke uitwerking.

    Delta2 = np.zeros(Theta1.shape)
    Delta3 = np.zeros(Theta2.shape)
    y_mat = get_y_matrix(y, y.shape[0])

    # Stap 1 - Forward propagation
    m, n = X.shape
    a1 = np.c_[np.ones(m), X]
    z2 = np.dot(a1, Theta1.T)
    a2 = sigmoid(z2)
    a2 = np.c_[np.ones(m), a2]
    z3 = np.dot(a2, Theta2.T)
    a3 = sigmoid(z3)

    for i in range(m):
        # Stap 2 - Bereken verschil tussen uitkomst (a3) en correcte waarden (y)
        d3 = (a3[[i],:] - y_mat[[i],:]).T

        # Stap 3 - Bereken de bijdrage aan totale fout van elke node
        d2 = np.multiply(np.dot(Theta2[:,1:].T, d3), sigmoidGradient(z2[[i],:].T))

        # Stap 4
        Delta3 = Delta3 + np.dot(d3, a2[[i],:])
        Delta2 = Delta2 + np.dot(d2, a1[[i],:])

    Delta2_grad = Delta2 / m
    Delta3_grad = Delta3 / m

    return Delta2_grad, Delta3_grad