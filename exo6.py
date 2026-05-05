texte=input("Entrez un texte ou un mot :")
compteur=0
for lettre in texte:
    if lettre=="a" or lettre=="e" or lettre=="i"or lettre=="o"or lettre=="u"or lettre=="A" or lettre=="E" or lettre=="I"or lettre=="O" or lettre=="U":
        compteur+=1
print("Nombre de voyelles :  ",compteur)
