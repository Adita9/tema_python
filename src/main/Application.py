# input_file = csv.DictReader(open("C://Users/aneagoe/PycharmProjects/Tema/anunturi.csv"), delimiter=";")
import csv
from datetime import datetime
import json
import operator
from xml.dom import minidom

import requests


# "C://Users/aneagoe/PycharmProjects/Tema/anunturi.csv"
def csv_to_dict(filename):
    reader = csv.reader(open(filename), delimiter=",")
    next(reader, None)
    input_file = sorted(reader,
                        key=operator.itemgetter(6))
    total_judete = {}
    for row in input_file[1:]:
        judet = row[6]
        valoare = row[11]
        if judet in total_judete:
            total_judete[judet] += float(valoare)
        else:
            total_judete[judet] = float(valoare)
    return total_judete


def total_judete_to_csv(filename, array):
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in array.items():
            writer.writerow([key, value])

def month_total_to_JSON(filename):
    total_luna = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            date = datetime.strptime(row[3], "%Y-%m-%dT%H:%M:%S")
            month = date.strftime('%B')
            if row[12] != 'RON' :
                value = convertor_to_RON(float(row[11]), row[12])
            else :
                value = float(row[11])
            if month in total_luna:
                total_luna[month] += value
            else:
                total_luna[month] = value
    with open('total.json', 'w') as file:
        json.dump(total_luna, file)


def convertor_to_RON(value, currency):
    response = requests.get("https://www.bnr.ro/nbrfxrates.xml")
    valori = minidom.parseString(response.content)
    rate = valori.getElementsByTagName('Rate')
    for rata in rate:
        schimbul_valutar = rata.attributes['currency'].value
        valoarea_schimbului = float(rata.firstChild.nodeValue)
        if currency == schimbul_valutar:
            value = float(value) * valoarea_schimbului
    return value

print(csv_to_dict("C://Users/aneagoe/PycharmProjects/Tema/anunturi.csv"))
total_judete_to_csv("total_pe_judete.csv",csv_to_dict("C://Users/aneagoe/PycharmProjects/Tema/anunturi.csv"))
# month_total_to_JSON("C://Users/aneagoe/PycharmProjects/Tema/anunturi.csv")
print(convertor_to_RON(50, "USD"))