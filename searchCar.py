#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import urllib.request

from bs4                                    import BeautifulSoup
from requests.packages.urllib3.exceptions   import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


carsfile    = "/tmp/searchCar"

freeUserId  = ""
freeUserPw  = ""


co2min      = 0
co2max      = 130
energie     = 'ess' #dies: diesel, ess: essence, electrique: elec, hybride: hyb, gpl: gpl, ethanol: eth, alternatif: alt, pour plusieur carburant: dies%2Cess (Separateur %2C)
model       = 'PEUGEOT%3A3008' #MARQUE%3AMODELE (Separateur %3A)
kmmin       = 0
kmmax       = 70000
pricemin    = 0
pricemax    = 13000
yearmin     = 2011
yearmax     = 2020
region      = "" #FR-ARA%2CFR-BFC


if __name__ == '__main__':

    url = 'https://www.lacentrale.fr/listing?co2Min=' + str(co2min) + '&co2Max=' + str(co2max) + '&energies=' + energie + '&makesModelsCommercialNames=' + model + '&mileageMin=' + str(kmmin) + '&mileageMax=' + str(kmmax) + '&priceMin=' + str(pricemin) + '&priceMax=' + str(pricemax) +'&yearMin=' + str(yearmin) + '&yearMax=' + str(yearmax) + '&regions=' + region

    r = requests.get(
            url,
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
            },
            verify=False
    )
    soup = BeautifulSoup(r.text, "lxml")

    cars = []
    try :
        with open(carsfile, 'r') as f:
            for line in f:
                uri = line.rstrip().lower()
                cars.append(uri)
    except:
        print (carsfile + " is not found")
        exit()



    for item in soup.find_all("div", {"class":"adContainer"} ):
        link            = item.find('a')
        linkUrl         = link.attrs['href']

        if linkUrl not in cars:
            linkDesc        = item.find('h3').find('span')
            linkDesc2       = linkDesc.findNext('span')
            title = linkDesc.text + linkDesc2.text

            f = open(carsfile, "a")
            f.write(linkUrl + "\n")
            f.close()

            message = urllib.parse.quote(title + " https://www.lacentrale.fr"+linkUrl, safe='')
            w = requests.get("https://smsapi.free-mobile.fr/sendmsg?user="+str(freeUserId)+"&pass="+str(freeUserPw)+"&msg="+message)
            print (title,linkUrl)
