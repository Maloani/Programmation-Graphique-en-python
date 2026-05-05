# =========================================
# EXERCICES PYTHON : VARIABLES - CONDITIONS - BOUCLES
# =========================================

# 1. Déterminer si un nombre est pair ou impair
n = int(input("Ex1 - Entrer un nombre : "))
if n % 2 == 0:
    print("Pair")
else:
    print("Impair")

print("\n------------------------\n")

# 2. Vérifier si un nombre est positif, négatif ou nul
n = int(input("Ex2 - Entrer un nombre : "))
if n > 0:
    print("Positif")
elif n < 0:
    print("Négatif")
else:
    print("Nul")

print("\n------------------------\n")

# 3. Trouver le plus grand de deux nombres
a = int(input("Ex3 - Entrer a : "))
b = int(input("Ex3 - Entrer b : "))
if a > b:
    print("Le plus grand est :", a)
else:
    print("Le plus grand est :", b)

print("\n------------------------\n")

# 4. Afficher la table de multiplication d’un nombre
n = int(input("Ex4 - Entrer un nombre : "))
for i in range(1, 11):
    print(n, "x", i, "=", n * i)

print("\n------------------------\n")

# 5. Calculer la somme des nombres de 1 à n
n = int(input("Ex5 - Entrer un nombre : "))
somme = 0
for i in range(1, n + 1):
    somme += i
print("Somme =", somme)

print("\n------------------------\n")

# 6. Afficher tous les nombres pairs entre 1 et 20
print("Ex6 - Nombres pairs entre 1 et 20 :")
for i in range(1, 21):
    if i % 2 == 0:
        print(i)

print("\n------------------------\n")

# 7. Vérification de mot de passe avec boucle
mot_de_passe = ""
while mot_de_passe != "python123":
    mot_de_passe = input("Ex7 - Entrer le mot de passe : ")
print("Accès autorisé")

print("\n------------------------\n")

# 8. Compter le nombre de voyelles dans un mot
mot = input("Ex8 - Entrer un mot : ")
compteur = 0
for lettre in mot:
    if lettre in "aeiouAEIOU":
        compteur += 1
print("Nombre de voyelles :", compteur)

print("\n------------------------\n")

# 9. Calculer la factorielle d’un nombre
n = int(input("Ex9 - Entrer un nombre : "))
fact = 1
for i in range(1, n + 1):
    fact *= i
print("Factorielle =", fact)

print("\n------------------------\n")

# 10. Jeu de devinette (nombre à trouver)
nombre_secret = 7
essai = 0
while essai != nombre_secret:
    essai = int(input("Ex10 - Devinez le nombre (1-10) : "))
print("Bravo !")