import requests
import random
import schedule
from datetime import datetime
import time 

def postdronesend(jsondata):
    
    r = requests.post('http://10.30.134.12:8011/api/drones', json=jsondata)  

def error():
    print("errore orrore")




#creo un metodo fittizio che simula il drone
def dronedemo():
    
    velocita = random.randrange(30000,70000) / 1000
    posizione = random.randrange(30000,70000) / 1000
    percentuale = random.randrange(1000,100000) / 1000
    data=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    idPersona = 1
    idDrone = 1
    print(data)
    json={
        "dueDate": data ,
        "posizione": posizione,
        "velocita": velocita,
        "percentuale": percentuale,
        "idPersona":idPersona,
        "idDrone":idDrone
    }
    postdronesend(json)




if __name__ == '__main__':
    #eseguo 
    schedule.every(1).minutes.do(dronedemo)
    while True:
           schedule.run_pending()
           time.sleep(1)
   