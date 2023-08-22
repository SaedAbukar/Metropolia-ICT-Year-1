#Käytin apuna tätä tutorialia: https://www.youtube.com/watch?v=rfscVS0vtbw
#Käytän try exceptiä, jotta varmistan, että käyttäjä lisää oikean arvon.
#Käytän while looppia, jotta käyttäjä voi vastata kysymkseen uudestaan, mikäli antaa väärän arvon.
#Oikean vastauksen jälkeen break outtaan while loopista.
while True:
    try:
        num1 = int(input('Lisää kokonaisluku: '))
        num2 = int(input('Lisää toinen kokonaisluku: '))
        num3 = int(input('Lisää kolmas kokonaislukua: '))
        break
    except ValueError:
        print('Et lisännyt kokonaislukua. Yritä uudestaan ja lisää kokonaisluku jokaiseen kohtaan.')
lukujen_summa = num1 + num2 + num3
lukujen_tulo = num1 * num2 * num3
lukujen_keskiarvo = int(lukujen_tulo) / 2

print('Lukujen summa on: ' + str(lukujen_summa))
print('Lukujen tulo on: ' + str(lukujen_tulo))
print('Lukujen keskiarvo on: ' + str(lukujen_keskiarvo))
