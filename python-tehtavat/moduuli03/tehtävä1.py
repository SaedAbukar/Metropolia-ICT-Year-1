
while True:
    try:
        kuhan_mitta = float(input('Mikä on kuhan pituus senttimetreinä? '))
        break
    except ValueError:
        print('Et lisännyt lukua. Lisää kuhan pituus luvuina.')

if kuhan_mitta < 37:
    ali_jaama = 37 - kuhan_mitta
    print(f'Kuha on alamittainen. Alimmasta sallitusta pyyntimitasta puuttuu {ali_jaama:.2f} cm')
    print('Laske kuha takaisin järveen.')
else:
    print('Hei, hieno pyydös!')
