import copy

from database.meteo_dao import MeteoDao
class Model:
    def __init__(self):
        self._sequenza=[]
        self.ggRimanenti=0


    def get_umiditaMediaPerMese(self,mese):
        dati = MeteoDao.get_all_situazioni()
        dati_torino = []
        dati_milano = []
        dati_genova = []

        for dato in dati:
            if dato.data.month == mese:
                if dato.localita == "Torino":
                    dati_torino.append(dato)
                elif dato.localita == "Milano":
                    dati_milano.append(dato)
                elif dato.localita == "Genova":
                    dati_genova.append(dato)

        result = [sum(i.umidita for i in dati_torino) / len(dati_torino),
                  sum(i.umidita for i in dati_milano) / len(dati_milano),
                  sum(i.umidita for i in dati_genova) / len(dati_genova)]
        return result

    def calcola_sequenza(self,mese):
        self.dati = MeteoDao.get_situazioniPerMese(mese)
        self._sequenza = [float('inf'),[]]
        self.ggMilano = 6
        self.ggTorino = 6
        self.ggGenova = 6
        self._livello = 0
        self._giorniRimanenti = 15
        self.costoParziale=0
        self.ricorsione(self.costoParziale,[], self._giorniRimanenti,self.ggMilano,self.ggGenova,self.ggTorino,self._livello)
        return (self._sequenza)
    def ricorsione(self,costoParziale,parziale,giorniRimanenti,ggMilano,ggGenova,ggTorino,livello):
        if giorniRimanenti == 0:
            if (costoParziale+self.calcolaSupplemento(parziale)) < self._sequenza[0]:
                self._sequenza=[copy.deepcopy(costoParziale)+self.calcolaSupplemento(parziale),copy.deepcopy(parziale)]
                print(self._sequenza)
                return
            else:
                return
        else:
            for i in range(livello * 3, (livello + 1) * 3):
                parziale.append(self.dati[i])
                giorniRimanenti-=1
                costoParziale+=self.dati[i].umidita
                if self.dati[i].localita=="Milano":
                    ggMilano-=1
                elif self.dati[i].localita=="Genova":
                    ggGenova-=1
                else:
                    ggTorino-=1

                if self.isAmmisibile(parziale,ggMilano,ggGenova,ggTorino,giorniRimanenti):
                    self.ricorsione(costoParziale,parziale,giorniRimanenti,ggMilano,ggGenova,ggTorino,livello+1)
                    print(parziale)


                giorniRimanenti += 1
                costoParziale -= self.dati[i].umidita
                if self.dati[i].localita == "Milano":
                    ggMilano += 1
                elif self.dati[i].localita == "Genova":
                    ggGenova += 1
                else:
                    ggTorino += 1
                parziale.pop()




    def isAmmisibile(self,parziale,ggMilano, ggGenova,ggTorino,ggRimanenti):
        if ggTorino<0 or ggMilano<0 or ggGenova<0 or ggRimanenti<0:
            return False
        if len(parziale) == 1:
            return True
        elif len(parziale) == 2:
            if parziale[-1].localita == parziale[-2].localita:
                return True
        elif len(parziale) >=3:
            permanenza = 0
            for i in parziale[-4:-1]:
                if i.localita == parziale[-2].localita:
                    permanenza+=1
            if permanenza<3 and parziale[-2].localita!=parziale[-1].localita:
                return False
            else:
                return True
        else:
            return False
    def calcolaSupplemento(self,sequenza):
        supplemento = 0
        for i in range(2,len(sequenza)):
            if sequenza[i].localita != sequenza[i-1].localita or sequenza[i].localita != sequenza[i-2].localita :
                supplemento+=100
        return supplemento







