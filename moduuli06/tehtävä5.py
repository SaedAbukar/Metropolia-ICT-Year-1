# Kirjoita funktio, joka saa parametrinaan listan kokonaislukuja.
# Ohjelma palauttaa toisen listan, joka on muuten samanlainen kuin parametrina saatu lista
# paitsi että siitä on karsittu pois kaikki parittomat luvut.
# Kirjoita testausta varten pääohjelma, jossa luot listan,
# kutsut funktiota ja tulostat sen jälkeen sekä alkuperäisen että karsitun listan.


def whole_numbers(integer):
    for i in integer:
        if i % 2 == 1:
            integer.remove(i)
    return integer


integer_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
print(whole_numbers(integer_list))
