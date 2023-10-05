import textwrap

story = """Olet Huuhkajien kapteeni. Saavuit Yhdysvaltoihin osallistuaksesi vuoden 2026 FIFAn MM-kisoihin.
Olet taistellut urhoollisesti karsintavaiheen läpi ja tehnyt maastasi ylpeän. Nyt alkaa todellinen taistelu!
Oletko valmis? Aloitit tiesi kunniaan ja kuuluisuuteen ensimmäiseltä lentokentältä.Olet päättänyt tuoda iloa ja tehdä maanmiehistäsi ylpeitä. 
Saavut ensimmäiselle jalkapallokentälle ja pidät siellä valmistautumisleirin. Jatkat sieltä seuraavalle kentälle pelaat siellä ensimmäisen rangaistuspotkukilpailusi. 
Pelaat viisaasti ja voitat Yhdysvallat, joka oli ensimmäinen vastustajasi. Pelaat loput lohkopelisi ja voitat kaksi ensimmäistä peliä. Varmistat itsellesi paikan pudotuspeleihin ja kolmanteen peliin menet rennolla fiiliksellä.
Pudotuspelivaihe alkaa ja nyt on kyllä kovan paikka. Se on Messin johtama Argentiina. Tiedät jo, että mikäli voitat heidät, palkinto tulee olemaan valtava. 
Menet sinne ja näytät heille, mistä olet tehty. Teet turnauksen ensimmäisen yllätyksen ja voitat heidät! Etenet 8-parhaan joukkoon.
Tarinan edetessä siirryt seuraaville lentokentille ja dominoit vastustajiasi. Viimein saavut jollekin jäljellä olevaan lentokenttään ja sieltä löydät viimeisen vastustajasi.
Finaali aika koittaa. Sinun ja maailmanmestaruuden välillä on enää yksi ottelu. Olet synnynnäinen voittaja, eikä häviö ole edes vaihtoehto, kuten olemme jo sen saaneet tietää,
Pelaat finaalin viileästi ja voitat sen. OLET MAAILMANMESTARI!!! Saavutit tavoitteesi ja voitit vastustajasi. Onnittelut!!!"""


story1 = textwrap.fill(story, 95)

rules = """Pelin nimi on Suomen MM-kisat. Peli on Jalkapallon MM-kisojen inspiroima. Pelin tarkoitus on kierrellä tulevien MM-kisojen jalkapallostadioneita ja etsiä vastustajia.
Pelin lähtöpiste arvotaan pelin alussa satunnaisesti. Pelin tarkoituksena on edetä lähtöpisteeltä ja löytää vastustajia eri kentiltä.
Vastustajia vastaan pelataan perinteinen rangaistuspotkukilpailu. MM-kisoissa finaalin asti selviytyneet pelaavat enintään seitsemän peliä.
Tässä pelissä on myös seitsemän ennalta määriteltyä vastustajaa. Pelissä edetään niin kuin MM-kisoissa ja tavoite on voittaa jokainen ottelu.
Pelin voittaa vain, jos etenee finaaliin asti ja voittaa finaalin. Pelin vastustajat on arvottu satunnaisesti pelin 16 eri jalkapallostadionille.
Pelaajan tehtävä on matkustella eri jalkapallostadioneille ja löytää vastustajat. Pelissä ei voi palata samalle lentokentälle tai pelata samaa vastustajaa vastaan uudestaan.
Pelissä on lohkovaihe ja pudotuspelivaihe. Lohkopelivaiheessa pitää voittaa vähintään kaksi peliä, jonka jälkeen siirryt pudotuspelivaiheeseen.
Jos et voita vähintään kaksi peliä, häviät pelin. Pudotuspelivaihe on kerrasta poikki. Pelin voittaa, jos etenee finaaliin asti ja voittaa finaalin."""


rules1 = textwrap.fill(rules, 95)



def get_story():
    max_width = max(len(line) for line in rules1.splitlines())
    print('+' + '-' * (max_width + 2) + '+')
    for line in story1.splitlines():
        print(f'| {line.ljust(max_width)} |')
    print('+' + '-' * (max_width + 2) + '+')


def get_rules():
    max_width = max(len(line) for line in rules1.splitlines())
    print('+' + '-' * (max_width + 2) + '+')
    for line in rules1.splitlines():
        print(f'| {line.ljust(max_width)} |')
    print('+' + '-' * (max_width + 2) + '+')

from colorama import Fore, Style

from colorama import Fore, Style

text = "Yhdysvaltojen"

# Color the text for USA in red, white, and blue
yhdysvallat = (
    Fore.RED + text[:4] +  # Color "Yhdysvalto" in red
    Fore.RESET + text[4:9] +  # Color "jen" in white
    Fore.BLUE + text[9:] +  # Color "n" in blue
    Fore.RESET  # Reset color to default
)



from colorama import Fore, Style

text = "Meksikon"

# Väritä teksti Meksikon lipun väreillä (vihreä, valkoinen, punainen)
meksiko = (
    Fore.GREEN + text[:3] +  # Väritä "Meksikon" vihreäksi
    Fore.RESET + text[3:6] +  # Jätä "on" valkoiseksi
    Fore.RED + text[6:] +  # Väritä "on" punaiseksi
    Fore.RESET  # Nollaa väri takaisin oletusarvoiseksi
)

from colorama import Fore, Style

text = "Kanadan"

# Color the text for Canada in red and white
kanada = (
    Fore.RED + text[:2] +  # Color "Kan" in red
    Fore.RESET + text[2:5] +  # Keep "adan" in white
    Fore.RED + text[5:] +  # Color "an" in red
    Fore.RESET  # Reset color to default
)
