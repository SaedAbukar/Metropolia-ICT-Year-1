# Kysyn käyttäjältä hyttiluokkaa

hytti = str.upper(input(f'Valitse hyttiluokka seuraavista vaihtoehdoista: LUX, A, B, C: '))


# Valinnan mukaan annan erilaiset vaihtoehdot

if hytti == 'LUX':
    print('LUX on parvekkeellinen hytti yläkannella.')
elif hytti == 'A':
    print('A on ikkunallinen hytti autokannen yläpuolella.')
elif hytti == 'B':
    print('B on ikkunaton hytti autokannen yläpuolella.')
elif hytti == 'C':
    print('C on ikkunaton hytti autokannen alapuolella.')
else:
    print('Virheellinen hyttiluokka')
