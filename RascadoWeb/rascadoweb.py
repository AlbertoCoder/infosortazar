"""
    MÓDULO PYTHON 3 PARA EL 'RASCADO WEB'
    Alberto Álvarez Portero ()

"""
from bs4 import BeautifulSoup
import requests


class Dato:

    def __init__(self,orig,eti,clase):

        self.origen = requests.get(orig).text
        self.intérprete = BeautifulSoup(self.origen,'lxml')
        self.tipo = self.intérprete.find_all(eti, attrs={'class':clase})


#origen = requests.get("https://lawebdelaprimitiva.com/Primitiva/Historico%20de%20sorteos.html").text


    def getFecha(self):

        return self.tipo[0].text 

    def getNums(self,n_tipos):
        
        combi_gan = []

        for tag in self.tipo[:n_tipos]:
            
            if(len(tag.text)==1):

                combi_gan.append("0%s" %tag.text)

            else:

                combi_gan.append(tag.text)

        return combi_gan  

