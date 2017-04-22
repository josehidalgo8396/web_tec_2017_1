import requests
import cssutils
import psycopg2
import time
from bs4 import BeautifulSoup

db = psycopg2.connect(database="d70j23m846rhsg", user="qprrzlbbnjntfc", password="2bc9e656799c9b685fbcf2ab4f3c170b3e03d21ce840e41358bbcff21461655c", host="ec2-50-19-95-47.compute-1.amazonaws.com", port="5432")
global registros
registros = 0
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

        second = soup.find("div", attrs={"id":"tekst1"})
        title = second.select("h1")
        if title[0].get_text() != "Tajo alto, Miramar 00":
            lista.append(title[0].get_text()) 

            fourth = soup.find("p", attrs={"id":"text2"})
            price = fourth.get_text()
            lista.append(price)

            mainArticle = soup.find("section", attrs={"class":"mainarticles"})

            characteristicsSection = mainArticle.select("div section")
            characteristics = characteristicsSection[0].select("ul li")
                
            for i in characteristics:
                if i.select("label")[0].get_text() != "Precio" and i.select("label")[0].get_text() != "precio" and i.select("label")[0].get_text() != "Caracteristicas internas" and i.select("label")[0].get_text() != "Caracteristicas Internas":
                    lista.append(i.select("p")[0].get_text())

            seenDiv = mainArticle.find("div", attrs={"class":"left"})
            seen = seenDiv.select("p")[0].get_text()
            seen = seen.split(" ")
            lista.append(seen[0])
            lista.append(seen[4] + " " + seen[5] + " " + seen[6])

            if len(lista) == 16:
                insertData(lista)

def insertData(lista):
    global registros
    query = ("insert into Registros(imagen, titulo, precio, tipo, venta, externas, superficie, tamano, camas, banos, mascotas, fechaConstruccion, ubicacion, tipoEdificio, visto, fechaVisto) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    lista[8] = lista[8].replace("+","")
    lista[9] = lista[9].replace("+","")
    houseData = tuple(lista)
    cursor = db.cursor()
    cursor.execute(query,houseData)
    db.commit()
    cursor.close()
    registros+=1

def main(link):
    global registros
    cont = 1
    while cont < 22:
        print("Pagina: " + str(cont))
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
    cursor = db.cursor()
    cursor.execute("insert into Auditoria(fecha, pagina_web, numero_registros, estado, errores) values(%s,%s,%s,%s,%s)",(time.strftime("%d-%m-%Y"), "https://www.casas.cr/c/casas/", registros, "finalizado", "no errors"))
    db.commit()
    cursor.close()
    print("Proceso terminado")

main("https://www.casas.cr/c/casas/")
