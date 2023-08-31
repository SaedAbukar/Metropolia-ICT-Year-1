# Kirjoita funktio, joka saa parametreinaan pyöreän pizzan halkaisijan senttimetreinä sekä pizzan hinnan euroina.
# Funktio laskee ja palauttaa pizzan yksikköhinnan euroina per neliömetri.
# Pääohjelma kysyy käyttäjältä kahden pizzan halkaisijat ja hinnat sekä ilmoittaa,
# kumpi pizza antaa paremman vastineen rahalle (eli kummalla on alhaisempi yksikköhinta).
# Yksikköhintojen laskennassa on hyödynnettävä kirjoitettua funktiota.


def pizza_value(diameter, euros):
    unit_price = euros / (diameter / 100)
    return unit_price


p1 = float(input('Syötä pizzan halkaisija senttimetreinä: '))
p1_price = float(input('Syötä pizzan hinta euroina: '))

p2 = float(input('Syötä pizzan halkaisija senttimetreinä: '))
p2_price = float(input('Syötä pizzan hinta euroina: '))

p1_unit_price = pizza_value(p1, p1_price)
p2_unit_price = pizza_value(p2, p2_price)

if p1_unit_price < p2_unit_price:
    print(f'Pizza 1 antaa paremman vastineen rahallesi:\n '
          f'{p1_unit_price:.2f} €/m2 on vähemmän kuin {p2_unit_price:.2f} €/m2.')
else:
    print(f'Pizza 2 antaa paremman vastineen rahallesi:\n'
          f'{p2_unit_price:.2f} €/m2 on vähemmän kuin {p1_unit_price:.2f} €/m2.')
