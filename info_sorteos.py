

"""
    INFORMACIÓN DE SORTEOS DEL ESETADO CON LCD CONECTADO A GPIO DE RPI4B
    Alberto Álvarez Portero
"""
import time
from datetime import datetime
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import RascadoWeb.rascadoweb as rascado
import os

#----------------------------VARIABLES Y CONSTANTES GLOBALES---------------------------------------------#

LCD_RS = 26
LCD_E = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11
LED_ON = 15

LCD_COLUMNS = 16
LCD_ROWS = 2

lcd = LCD.Adafruit_CharLCD(
    LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7,
    LCD_COLUMNS, LCD_ROWS
)

URL_SORTEOS_PRIMITIVA = "https://lawebdelaprimitiva.com/Primitiva/Historico%20de%20sorteos.html"
URL_PREMIOS_PRIMITIVA = "https://www.labrujadeoro.es/primitiva-premios.htm"
URL_SORTEOS_EUROMILLONES = "https://lawebdelaprimitiva.com/Euromillones/Historico%20de%20sorteos.html"
BOLA_BLANCA = 'blanca'
COMPLEMENTARIO = 'comple'
REINTEGRO = 'reintegro'
JOKER = 'joker'
ARCHIVO_PRIMITIVA = "primitiva.txt"


primitiva_nums = rascado.Dato(URL_SORTEOS_PRIMITIVA,'li',BOLA_BLANCA)
primitiva_comp = rascado.Dato(URL_SORTEOS_PRIMITIVA,'li',COMPLEMENTARIO)
primitiva_reint = rascado.Dato(URL_SORTEOS_PRIMITIVA,'li',REINTEGRO)
primitiva_joker = rascado.Dato(URL_SORTEOS_PRIMITIVA,'li',JOKER)
primitiva_premio = rascado.Dato(URL_PREMIOS_PRIMITIVA,'td','c2')
global reintegro_acertado

modo_comprobar = True
nums_primi_jugados = []
joker_jugado = 0
nums_primi_acertados = []


euromillo_nums = rascado.Dato(URL_SORTEOS_EUROMILLONES,'li','blanca')
euromillo_estr = rascado.Dato(URL_SORTEOS_EUROMILLONES,'li','estrella')

global nums_euromi_jugados


interrogapertura = [

	0b100,0b0,0b100,0b1000,0b10001,0b10001,0b1110,0b00000

]


custom_char = [
  0b00000,
  0b00100,
  0b01110,
  0b11111,
  0b11111,
  0b01110,
  0b00100,
  0b00000
]


#------------------------------FUNCIONES GLOBALES--------------------------------------------------#


def mostrar_menu_opc():

    elec_comprobar = input("¿Quieres comprobar tus números? (Sí/No): ")

    if(elec_comprobar == "Sí"):

        modo_comprobar = True

        print("\n")
        
        sele = input("1.- Lotería Primitiva\n\n2.- Euromillones\n\n3.- Ambos sorteos\n\n\tElección: ")
       
        while sele not in ("1","2","3"):

            mostrar_menu_opc()

        if(sele=="1"):
    
            print("\n")
            introduce_nums_primi()

        elif(sele=="2"):
            print("\n")
            #introduce_nums_eurom()

        else:
            print("\n")
            introduce_nums_primi()
            #introduce_nums_eurom()


def leer_archivo_nums_jugados(archivo):

    # Abrir archivo para lectura.
    with open(archivo, "r") as f:
        # Inicializar una lista vacía para almacenar las líneas.
        
        # Iterar cada línea del archivo.
        for l_inea in f:
            # Eliminar los caracteres en blanco de cada línea y añadirlas a la lista.
            nums_primi_jugados.append(l_inea.strip())

    print("Has jugado los siguientes números a 'La Primitiva':\n")

    for i_ndice,columna in enumerate(nums_primi_jugados):

        print("Columna %d: %s" %(i_ndice,columna))
    
    f.close()

def introduce_nums_primi():

    leer_archivo_nums_jugados(ARCHIVO_PRIMITIVA)


''' 
def introduce_nums_eurom():

    interac_usuario = input("Por favor, introduce los 4 números y las 2 estrellas, separados por espacios: ")

    for i in interac_usuario.split(" "):
        
        nums_euromi_jugados.append(i)
    
    print(nums_primi_acertados)
'''

def mostrarPrimitiva():
    '''
    Muestra la información del sorteo de la primitiva en una pantalla de 16 columnas y 2 filas.
    '''

    lcd.message(" %s %s %s   c%s\n %s %s %s   r%s" %(primitiva_nums.getNums(6)[0],
                                      primitiva_nums.getNums(6)[1],
                                      primitiva_nums.getNums(6)[2],
                                      primitiva_comp.getNums(1)[0],
                                      primitiva_nums.getNums(6)[3],
                                      primitiva_nums.getNums(6)[4],
                                      primitiva_nums.getNums(6)[5],
                                      primitiva_reint.getNums(1)[0]))

def comprobarPrimitiva():

    lista_columna_acertados = []

    singular_plural = "aciertos"
     
    for i,columna in enumerate(nums_primi_jugados):
       
        for j,num in enumerate(columna.split(",")):

            if num in primitiva_nums.getNums(7) and j<6:
             
                lista_columna_acertados.append(num)
        
        nums_primi_acertados.append(lista_columna_acertados)
        
        time.sleep(2)
        lcd.clear()
        lcd.home()

        if(len(lista_columna_acertados)==1):

            singular_plural = "acierto"
        
        else:

            singular_plural = "aciertos"

        lcd.message(" Columna %d prim:\n %d %s." %(i+1,len(nums_primi_acertados[i]),singular_plural))
        time.sleep(3)        
        print(lista_columna_acertados)
         
        lista_columna_acertados.clear()

    time.sleep(5)

    nums_primi_acertados.clear()
    print(nums_primi_jugados)
    print(nums_primi_acertados) 
    
def comprobarReintegro():

    print("Números: %s" %(nums_primi_jugados))
    print("Reintegro: %s" %primitiva_reint.getNums(1)[0])
    if nums_primi_jugados[0].split(",")[6] == primitiva_reint.getNums(1)[0]:
       
        print("Has acertado el reintegro.")
        lcd.clear()
        lcd.message("   REINTEGRO    \n    ACERTADO     ")
        time.sleep(10)
        lcd.clear()
        lcd.home()

def mostrarPremioPrimi():

    if(len(nums_primi_acertados) == primitiva_premio):

        lcd.message("Premio: %s" %primitiva_premio)

def mostrarJoker():

    lcd.message(" JOKER: %s " %primitiva_joker.getNums(1)[0])


def mostrarEuromillones():
    
    '''
    Muestra la información del sorteo de euromillones en una pantalla de 16 columnas y 2 filas.
    '''

     
    lcd.message(" %s %s %s %s %s\n    e%s  e%s   " %(euromillo_nums.getNums(5)[0],
                                      euromillo_nums.getNums(5)[1],
                                      euromillo_nums.getNums(5)[2],
                                      euromillo_nums.getNums(5)[3],
                                      euromillo_nums.getNums(5)[4],
                                      euromillo_estr.getNums(2)[0],
                                      euromillo_estr.getNums(2)[1]))

def imprime_mens(mens):
    print(mens)

def informar_nuevo_sorteo(juego,retardo):
    """
    Informa sobre el nuevo sorteo celebrado parpadeando el texto.

    Parámetros
    ----------
        juego : str
            Nombre del sorteo celebrado.
        retardo : Float
            Tiempo de muestra del mensaje.
    """  
    for i in range(1,10):
        
        i+=1
        lcd.message("   HA SALIDO\n  %s" %juego)
        time.sleep(retardo)
        lcd.clear()
        time.sleep(retardo/2)


#-----------------------------FUNCIÓN PRINCIPAL------------------------------------------------------------#



def main():
    
    lcd.show_cursor(False)
    lcd.create_char(0, interrogapertura)
    mostrar_menu_opc()

    while True:
        
        fecha_primi = rascado.Dato("https://lawebdelaprimitiva.com/Primitiva.html",'time','published')
        fecha_eurom = rascado.Dato("https://lawebdelaprimitiva.com/Euromillones.html",'time','published')
        
        lcd.home()
        hoy = datetime.today()
        time.sleep(1) #Aquí hago una suspensión de 1 segundo para dar tiempo a la asignación de variable.
        hoy_formateado = hoy.strftime("%d")
        time.sleep(1) #Aquí hago una suspensión de 1 segundo para dar tiempo a la asignación de variable.
        
        print(hoy)
        print(fecha_primi.getFecha())


        if(int(fecha_primi.getFecha().split(" ")[1])==int(hoy_formateado)):

            informar_nuevo_sorteo("LA PRIMITIVA",0.5)
            print("¡Ha salido un nuevo sorteo de La Primitiva!") 
        
        if(int(fecha_eurom.getFecha().split(" ")[1])==int(hoy_formateado)):

            informar_nuevo_sorteo("EUROMILLONES",0.5)
            print("¡Ha salido un nuevo sorteo de Euromillones!") 

        lcd.message("Sorteo Primitiva\n    %s %s" %(fecha_primi.getFecha().split(" ")[0],fecha_primi.getFecha().split(" ")[1]))
         
        time.sleep(3)
        
        lcd.clear()
         
        mostrarPrimitiva()
        
        
        print("----------------\n") 
        print("Sorteo Primitiva\n    %s %s\n" %(fecha_primi.getFecha().split(" ")[0],fecha_primi.getFecha().split(" ")[1]))
        print(" %s %s %s   c%s\n %s %s %s   r%s\n" %(primitiva_nums.getNums(6)[0],
                                          primitiva_nums.getNums(6)[1],
                                          primitiva_nums.getNums(6)[2],
                                          primitiva_comp.getNums(1)[0],
                                          primitiva_nums.getNums(6)[3],
                                          primitiva_nums.getNums(6)[4],
                                          primitiva_nums.getNums(6)[5],
                                          primitiva_reint.getNums(1)[0]))

        time.sleep(15)
       
        lcd.clear()
        
        mostrarJoker()
        
        time.sleep(10)
         
        comprobarPrimitiva()
        
        time.sleep(5)
      
        comprobarReintegro()
       
        time.sleep(10)

        lcd.clear()

        lcd.message("  Euromillones  \n    %s %s" %(fecha_eurom.getFecha().split(" ")[0],fecha_eurom.getFecha().split(" ")[1]))
        
        time.sleep(3)
        
        lcd.clear()
     
        mostrarEuromillones()
        
        print("-------------------\n") 
        print("Sorteo Euromillones\n    %s %s\n" %(fecha_eurom.getFecha().split(" ")[0],fecha_eurom.getFecha().split(" ")[1])) 
        print(" %s %s %s %s %s\n    e%s  e%s   \n" %(euromillo_nums.getNums(5)[0],
                                          euromillo_nums.getNums(5)[1],
                                          euromillo_nums.getNums(5)[2],
                                          euromillo_nums.getNums(5)[3],
                                          euromillo_nums.getNums(5)[4],
                                          euromillo_estr.getNums(2)[0],
                                          euromillo_estr.getNums(2)[1]))
        time.sleep(15)

        lcd.clear()
        
        os.system('clear')
        
        imprime_mens("----------------------------------------------------------\n")
        imprime_mens("EXTRACTOR DE INFORMACIÓN DE LOTERÍAS Y APUESTAS DEL ESTADO.\n\t\tAlberto Álvarez Portero")
        imprime_mens("----------------------------------------------------------\n")

main()        
#GPIO.cleanup()
