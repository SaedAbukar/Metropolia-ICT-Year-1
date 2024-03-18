# Kirjoita funktio, joka saa parametrinaan bensiinin määrän Yhdysvaltain nestegallonoina
# ja palauttaa paluuarvonaan vastaavan litramäärän.
# Kirjoita pääohjelma, joka kysyy gallonamäärän käyttäjältä ja muuntaa sen litroiksi.
# Muunnos on tehtävä aliohjelmaa hyödyntäen.
# Muuntamista jatketaan siihen saakka, kunnes käyttäjä syöttää negatiivisen gallonamäärän.
# Yksi gallona on 3,785 litraa.

def gallon_to_litre(gallon):
    gallon = float(gallon) * 3.785
    return gallon


user_gallon = (input('Syötä bensiinin määrä nestegallonoina tai paina Enteriä ohjelman lopettamiseksi: '))

while user_gallon != '':
    print(f'{user_gallon} nestegallonia on {gallon_to_litre(user_gallon):.3f} litraa')
    user_gallon = (input('Syötä bensiinin määrä nestegallonoina tai paina Enteriä ohjelman lopettamiseksi: '))

else:
    print('Painoit Enteriä. Ohjelma lopetettu.')
