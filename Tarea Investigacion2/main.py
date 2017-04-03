import requests
import cssutils
import MySQLdb
from bs4 import BeautifulSoup

db = MySQLdb.connect(host="localhost",user="root",passwd="12345",db="mydbScrap")
db.set_character_set('utf8')

def getData(link):
    lista = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    first = soup.find("div", attrs={"class":"housesale"})
    if first != None:
        imageDiv = first.select("div div")
        image = imageDiv[0]["style"]
        image = image[22:-3]
        if len(image) > 200:
            image = "no image"
        lista.append(image)
        #print(image)

        second = soup.find("div", attrs={"id":"tekst1"})
        title = second.select("h1")
        if title[0].get_text() != "Tajo alto, Miramar 00":
            lista.append(title[0].get_text()) #caracteristicas internas
            #print(title[0].get_text())

            fourth = soup.find("p", attrs={"id":"text2"})
            price = fourth.get_text()
            lista.append(price)
            #print(price)

            mainArticle = soup.find("section", attrs={"class":"mainarticles"})

            characteristicsSection = mainArticle.select("div section")
            characteristics = characteristicsSection[0].select("ul li")
                
            for i in characteristics:
                if i.select("label")[0].get_text() != "Precio" and i.select("label")[0].get_text() != "precio" and i.select("label")[0].get_text() != "Caracteristicas internas" and i.select("label")[0].get_text() != "Caracteristicas Internas":
                    lista.append(i.select("p")[0].get_text())
                    #print(i.select("p")[0].get_text())

            seenDiv = mainArticle.find("div", attrs={"class":"left"})
            seen = seenDiv.select("p")[0].get_text()
            seen = seen.split(" ")
            lista.append(seen[0])
            lista.append(seen[4] + " " + seen[5] + " " + seen[6])
            #print(seen)
            #print(lista)
            if len(lista) == 16:
                print("Imagen: " + lista[0])
                print("Titulo: " + lista[1])
                print("Precio: " + lista[2])
                print("Tipo: " + lista[3])
                print("Compra o Alquiler: " + lista[4])
                print("Caracteristicas externas: " + lista[5])
                print("Superficie: " + lista[6])
                print("Tamaño: " + lista[7])
                print("Camas: " + lista[8])
                print("Baños: " + lista[9])
                print("Mascotas: " + lista[10])
                print("Fecha de Construccion: " + lista[11])
                print("Ubicacion: " + lista[12])
                print("Tipo de Edificio: " + lista[13])
                print("Visto: " + lista[14] + " veces")
                print("Ultima fecha de visto: " + lista[15])
                print("\n\n")

def main(link):
    cont = 1
    while cont < 22:
        print("Pagina: " + str(cont))
        print("------------------------------------------------------------------------------------------------")
        if cont == 1:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, "html.parser")
            houses = soup.findAll("a", attrs={"class":"houses"})
            for i in houses:
                getData(link+i["href"][9:])
        else:
            newLink = link+"p/"+str(cont)+"/"
            page = requests.get(newLink)
            soup = BeautifulSoup(page.content, "html.parser")
            houses = soup.findAll("a", attrs={"class":"houses"})
            for i in houses:
                getData(link+i["href"][9:])
        cont+=1
    print("Proceso terminado")

main("https://www.casas.cr/c/casas/")
