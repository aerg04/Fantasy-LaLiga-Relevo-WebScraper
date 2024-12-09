import requests
from bs4 import BeautifulSoup
import json
import os

# Replace 'URL' with the actual URL of the webpage you want to scrape
class Scraper:
    @staticmethod
    def getPlayersUrl():
        urls = [
        "https://www.futbolfantasy.com/laliga/equipos/alaves",
        "https://www.futbolfantasy.com/laliga/equipos/athletic",
        "https://www.futbolfantasy.com/laliga/equipos/atletico",
        "https://www.futbolfantasy.com/laliga/equipos/barcelona",
        "https://www.futbolfantasy.com/laliga/equipos/betis",
        "https://www.futbolfantasy.com/laliga/equipos/celta",
        "https://www.futbolfantasy.com/laliga/equipos/espanyol",
        "https://www.futbolfantasy.com/laliga/equipos/getafe",
        "https://www.futbolfantasy.com/laliga/equipos/girona",
        "https://www.futbolfantasy.com/laliga/equipos/las-palmas",
        "https://www.futbolfantasy.com/laliga/equipos/leganes",
        "https://www.futbolfantasy.com/laliga/equipos/mallorca",
        "https://www.futbolfantasy.com/laliga/equipos/osasuna",
        "https://www.futbolfantasy.com/laliga/equipos/rayo-vallecano",
        "https://www.futbolfantasy.com/laliga/equipos/real-madrid",
        "https://www.futbolfantasy.com/laliga/equipos/real-sociedad",
        "https://www.futbolfantasy.com/laliga/equipos/sevilla",
        "https://www.futbolfantasy.com/laliga/equipos/valencia",
        "https://www.futbolfantasy.com/laliga/equipos/valladolid",
        "https://www.futbolfantasy.com/laliga/equipos/villarreal"
        ]
        if not os.path.exists("files/players.txt"):
            for url in urls:
                try:
                    # Send HTTP request to the webpage
                    response = requests.get(url.rstrip())
                except Exception as e:
                    print(e)
                    return
                # Parse HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all <a> tags with the class 'juggador pos-0 flex-column'
                a_tags = soup.find_all('a', class_='juggador pos-0 flex-column')

                # Extract and print the href attribute of each <a> tag
                hrefs = list({a['href'] for a in a_tags if 'href' in a.attrs})

                with open("files/players.txt", "a",encoding="utf-8") as f:
                    f.write(json.dumps(hrefs,ensure_ascii=False)+'\n')
            print("ready players urls")

    @staticmethod
    def getPlayersInfo(url:str):
        try:
            response = requests.get(url)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #quiero el nombre
            name = soup.find('h1', class_='display-initial').text
            
            if(name.find(".")!=-1):
                
                #hay jugadores que no tienen su nombre de pila"
                name = name.split(".")[1].lstrip()
            #quiero el equipo
            team = soup.find("div", "img-underphoto col-12 col-md-6 info border-0 font-weight-bold text-center mt-2 mb-0 pb-0 mt-md-0")
            #quiero la posicion
            team = team.text.strip()
            div_tag = soup.find('div', class_='mx-2 mb-3 text-center mt-1')
            position = div_tag.find('span').text
            #quiero los puntos
            span_elements = soup.find_all('span', class_=lambda x: x and 'laliga-fantasy' in x)
            points = []
            for span in span_elements:
                try:
                    points.append(int(str(span.text).replace('\n', '').strip()))
                except:
                    points.append(0)
            return [team,name,position,points]
        except Exception as e:
            print(e,e.add_note)

if __name__ == "__main__":
    Scraper.getPlayersUrl()
    