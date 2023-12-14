# Kirjoita while-toistorakennetta käyttävä ohjelma,
# joka tulostaa kolmella jaolliset luvut väliltä 1..1000

i = 1
while i <= 1000:
    if i % 3 == 0:
        print(i)
    i += 1
