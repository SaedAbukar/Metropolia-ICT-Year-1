import textwrap

story = """Olet Huuhkajien kapteeni. Saavuit Yhdysvaltoihin osallistuaksesi vuoden 2026 FIFAn MM-kisoihin.
Olet taistellut urhoollisesti karsintavaiheen läpi ja tehnyt maastasi ylpeän. Nyt alkaa todellinen taistelu!
Oletko valmis? Aloitit tiesi kunniaan ja kuuluisuuteen ensimmäiseltä lentokentältä.
Olet päättänyt tuoda iloa ja tehdä maanmiehistäsi ylpeitä. Laskeudut ensimmäiselle lentokentällesi ja pelaat siellä
ensimmäisen rangaistuspotkukilpailusi. Pelaat viisaasti ja voitat Yhdysvallat, joka oli ensimmäinen vastustajasi.
Valitettavasti he eivät olleet mahtavin vastustaja, joten sait minimipisteet, joka on 100 pistettä.
Siirryt seuraavalle lentokentälle ja nyt on kyllä kovan paikka. Se on Messin johtama Argentiina. Tiedät jo, että mikäli voitat heidät,
palkinto tulee olemaan valtava. Menet sinne ja näytät heille, mistä olet tehty. Teet turnauksen ensimmäisen yllätyksen ja voita heidät! Sait palkkioksi 1200 pistettä!! Tarinan edetessä siirryt seuraaville lentokentille ja
dominoit vastustajiasi. Viimein saavut jollekin jäljellä olevaan lentokenttään ja sieltä löydät viimeisen vastustajasi.
Jos voitat heidät, saavutat pelin tavoitteen, joka on saavuttaa yhteensä 5000 pistettä. Kuten olemme jo saaneet tietää,
et ole häviäjä ja voitat viimeisen pelin. OLET MAAILMANMESTARI!!! Saavutit tavoitteesi ja voitit vastustajasi.
Sait myös maksimipisteen, joka on 5000. Onnittelut!!!"""


wrapper = textwrap.TextWrapper(width=5000, break_long_words=False, replace_whitespace=False)

word_list = wrapper.wrap(text=story)


def get_story():
    return word_list
