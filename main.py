from scraper import Scraper
import threading
import json
import time

class Main:
    @staticmethod
    def main():
        Main.savePlayersData()
        pass
    
    @staticmethod
    def savePlayersData():
        playersdata = []
        lock = threading.Lock()

        #garantiza tener txt creado
        Scraper.getPlayersUrl()

        def iterateLinks(urls:list):
            data_list = []
            starttime = time.time()
            for url in urls:
                player_info = Scraper.getPlayersInfo(url)
                data_list.append(player_info)
            with lock:
                playersdata.extend(data_list)
            endtime = time.time()
            print(f"Thread {threading.current_thread().name} finished. Time: {endtime-starttime} ")


        threads = []
        with open("files/players.txt", "r") as f:
            for line in f:
                data = json.loads(line)
                t = threading.Thread(target=iterateLinks, args=(data,))
                threads.append(t)
                t.start()

        #espera a que todos los threads terminen
        for t in threads:
            t.join()
            #print(t.name)

        with open("files/playersdata.txt", "w",encoding="utf-8") as f:
            f.write(json.dumps(playersdata,indent=4,ensure_ascii=False))


if __name__ == "__main__":
    Main.main()