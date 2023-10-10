import textwrap
from colorama import Fore

story = """Olet Huuhkajien kapteeni. Saavuit Yhdysvaltoihin osallistuaksesi vuoden 2026 FIFAn MM-kisoihin.
Olet taistellut urhoollisesti karsintavaiheen läpi ja tehnyt maastasi ylpeän. Nyt alkaa todellinen taistelu!
Oletko valmis? Aloitit tiesi kunniaan ja kuuluisuuteen ensimmäiseltä lentokentältä.Olet päättänyt tuoda iloa ja tehdä maanmiehistäsi ylpeitä. 
Saavut ensimmäiselle jalkapallokentälle ja pidät siellä valmistautumisleirin. Jatkat sieltä seuraavalle kentälle ja pelaat siellä ensimmäisen rangaistuspotkukilpailusi. 
Pelaat viisaasti ja voitat Yhdysvallat, joka oli ensimmäinen vastustajasi. Pelaat loput lohkopelisi ja voitat kaksi ensimmäistä peliä. Varmistat itsellesi paikan pudotuspeleihin ja kolmanteen peliin menet rennolla fiiliksellä.
Pudotuspelivaihe alkaa ja nyt on kyllä kovan paikka. Se on Messin johtama Argentiina. Tiedät jo, että mikäli voitat heidät, palkinto tulee olemaan valtava. 
Menet sinne ja näytät heille, mistä olet tehty. Teet turnauksen ensimmäisen yllätyksen ja voitat heidät! Etenet 8-parhaan joukkoon.
Tarinan edetessä siirryt seuraaville lentokentille ja dominoit vastustajiasi. Viimein saavut jollekin jäljellä olevaan lentokenttään ja sieltä löydät viimeisen vastustajasi.
Finaali aika koittaa. Sinun ja maailmanmestaruuden välillä on enää yksi ottelu. Olet synnynnäinen voittaja, eikä häviö ole edes vaihtoehto, kuten olemme jo sen saaneet tietää,
Pelaat finaalin viileästi ja voitat sen. OLET MAAILMANMESTARI!!! Saavutit tavoitteesi ja voitit vastustajasi. Onnittelut!!!"""


story1 = textwrap.fill(story, 95)

rules = """Pelin nimi on Suomen MM-kisat. Peli on Jalkapallon MM-kisojen inspiroima. Pelin tarkoitus on kierrellä tulevien MM-kisojen jalkapallostadioneita ja etsiä vastustajia.
Pelin lähtöpiste arvotaan pelin alussa satunnaisesti. Pelin tarkoituksena on edetä lähtöpisteeltä ja löytää vastustajia eri kentiltä. Jokainen matkustuskerta lisää CO2 päästöjä 200. Yksi pelin tavoitteista on tuottaa mahdollisimman vähän päästöjä.
Mitä vähemmillä matkustuskerroilla löydät vastustajat, sitä parempi. Vastustajia vastaan pelataan perinteinen rangaistuspotkukilpailu. MM-kisoissa finaalin asti selviytyneet pelaavat enintään seitsemän peliä.
Tässä pelissä on myös seitsemän ennalta määriteltyä vastustajaa. Pelissä edetään niin kuin MM-kisoissa ja tavoite on voittaa jokainen ottelu.
Pelin voittaa vain, jos etenee finaaliin asti ja voittaa finaalin. Pelin vastustajat on arvottu satunnaisesti pelin 16 eri jalkapallostadionille.
Pelaajan tehtävä on matkustella eri jalkapallostadioneille ja löytää vastustajat. Pelissä ei voi palata samalle lentokentälle tai pelata samaa vastustajaa vastaan uudestaan.
Pelissä on lohkovaihe ja pudotuspelivaihe. Lohkopelivaiheessa pitää voittaa vähintään kaksi peliä, jonka jälkeen siirryt pudotuspelivaiheeseen.
Jos et voita vähintään kaksi peliä, häviät pelin. Pudotuspelivaihe on kerrasta poikki. Pelin voittaa, jos etenee finaaliin asti ja voittaa finaalin. Pelissä ei
ole pronssiottelua tai mitaleita muista sijoista."""


rules1 = textwrap.fill(rules, 95)



def get_story():
    max_width = max(len(line) for line in story1.splitlines())
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


text = "Yhdysvaltojen"

# Väritä yhdysvaltojen väreillä punainen, valkoinen ja sininen
yhdysvallat = (
    Fore.RED + text[:4] +  # Väritä "Yhdy" punaisella
    Fore.RESET + text[4:9] +  # Väritä "svalt" valkoisella
    Fore.BLUE + text[9:] +  # Väritä "ojen" sinisellä
    Fore.RESET  # Nollaa väri takaisin oletusarvoiseksi
)


text = "Meksikon"

# Väritä teksti Meksikon lipun väreillä (vihreä, valkoinen, punainen)
meksiko = (
    Fore.GREEN + text[:3] +  # Väritä "Mek" vihreäksi
    Fore.RESET + text[3:6] +  # Jätä "si" valkoiseksi
    Fore.RED + text[6:] +  # Väritä "kon" punaiseksi
    Fore.RESET  # Nollaa väri takaisin oletusarvoiseksi
)


text = "Kanadan"

# Väritä teksti Kanadan lipun väreillä punainen ja valkoinen
kanada = (
    Fore.RED + text[:2] +  # Väritä "Ka" punaisella
    Fore.RESET + text[2:5] +  # Väritä "nad" valkoisella
    Fore.RED + text[5:] +  # Väritä "an" punaisella
    Fore.RESET  # Nollaa väri takaisin oletusarvoiseksi
)


text = """
  ____  _   _  ___  __  __ _____ _   _     __  __ __  __       _  _____ ____    _  _____ 
 / ___|| | | |/ _ \|  \/  | ____| \ | |   |  \/  |  \/  |     | |/ /_ _/ ___|  / \|_   _|
 \___ \| | | | | | | |\/| |  _| |  \| |   | |\/| | |\/| |_____| ' / | |\___ \ / _ \ | |  
  ___) | |_| | |_| | |  | | |___| |\  |   | |  | | |  | |_____| . \ | | ___) / ___ \| |  
 |____/ \___/ \___/|_|  |_|_____|_| \_|   |_|  |_|_|  |_|     |_|\_\___|____/_/   \_\_|  
"""

# Suomen lipun värit: sininen ja valkoinen
colors = [Fore.BLUE, Fore.WHITE]

# Väritetään teksti Suomen lipun väreissä
colored_text = ""
color_idx = 0  # Indeksi värien vaihtamiseksi

for char in text:
    if char.isalpha():
        # Väritetään kirjaimet Suomen lipun väreissä
        colored_text += f"{colors[color_idx % len(colors)]}{char}"
        color_idx += 1
    else:
        # Jätetään muut merkit alkuperäisessä värissään
        colored_text += char


trophy = '🏆'
sad_emoji = "\U0001F622"
smiley_emoji = "\U0001F604"
fanfare_emoji = "\U0001F389"
number1_emoji = "\U0001F947"
football_emoji = "\u26BD"
airplane_emoji = "\u2708"
takeoff_airplane_emoji = "\U0001F6EB"
landing_airplane_emoji = "\U0001F6EC"
check_mark_emoji = "\u2713"
x_emoji = "\u274C"
stadium_emoji = '🏟️'
next_emoji = '➡️'
statue_of_liberty_emoji = '🗽'
cactus_emoji = '🌵'
maple_emoji = '🍁'
diagram_emoji = '📊'
co2_emoji = '🌍🏭'
