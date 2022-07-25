

import sys
import time
import telepot
import RPi.GPIO as GPIO
from datetime import datetime
#LED
def on(pin):
        GPIO.output(pin,GPIO.HIGH)
        return
def off(pin):
    
        GPIO.output(pin,GPIO.LOW)
        return
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
pin_out=11
filename="registro_bot.txt"
filename2="menu.txt"
filename3="Estado_Auto.csv"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_out,GPIO.OUT)
Espera=2
pin_in=16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_in,GPIO.IN)
ESTADO_PLANTA='SECO'
GPIO.output(pin_out,GPIO.HIGH)
csv=open (filename3,'w')
csv.truncate(4)
csv.write("False")
csv.close
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print('mensajes: %s' % command)
    valor=GPIO.input(pin_in)
    if   valor ==0: 
         ESTADO_PLANTA='HUMEDO'
    else:
         ESTADO_PLANTA='SECO'         
    comando_upper=command.upper()
    #Registrolog(comando_upper,chat_id) 
    if comando_upper == 'HOLA' or comando_upper == 'HI' or comando_upper == 'HOLA KRLOSBOT' or comando_upper == 'HOLI':
        txt=open (filename2)
        lectura_menu=txt.read()
        bot.sendMessage(chat_id, 'Hola '+msg['chat']['first_name'])
        bot.sendMessage(chat_id, lectura_menu)

    elif comando_upper =='HUMEDAD':
        bot.sendMessage(chat_id, "El estado de la planta actual es: "+ESTADO_PLANTA)
    elif comando_upper =='HISTORIAL':
        txt2=open (filename)
        lectura_Historico=txt2.read()
        bot.sendMessage(chat_id, "El historial del procesos es el siguiente: \n")
        bot.sendMessage(chat_id, lectura_Historico)
        Archivo=open(filename, "rb")
        bot.sendDocument(chat_id,Archivo)
    elif comando_upper =='RIEGO':
        txt2=open (filename)
        lectura_Historico=txt2.read()
        bot.sendMessage(chat_id, "Oprime ON para encerder la bomba por 5 segundos: \n")
    elif comando_upper =='AUTO_ON':
        bot.sendMessage(chat_id, "Modo Automatico Activo \n")
        print("Modo AUTO ON ")
        Cambio_Estado("True")
    elif comando_upper =='AUTO_OFF':
        bot.sendMessage(chat_id, "Modo Automatico Desactivado \n")
        print("Modo AUTO OFF ")
        Cambio_Estado("False")
    elif comando_upper =='RECOLECCION':
        bot.sendMessage(chat_id, "Consultando recoleccion del dia\n")
        bot.sendMessage(chat_id, "Ingreso hoy los usuarios \n")
        bot.sendMessage(chat_id, "CarlosP \n")
        bot.sendMessage(chat_id, "CamilaG \n")
        print("Datos recoleccion")

    elif comando_upper =='OFF':
        GPIO.output(pin_out,GPIO.HIGH)
        bot.sendMessage(chat_id, "Bomba Desactivada \n")
    elif comando_upper =='ON':
        GPIO.output(pin_out,GPIO.LOW)
        bot.sendMessage(chat_id, "Bomba Activada: \n")
        time.sleep(5)
        valor=GPIO.input(pin_in)
        if   valor ==0: 
          ESTADO_PLANTA='HUMEDO'
        else:
           ESTADO_PLANTA='SECO'  
        bot.sendMessage(chat_id, "Finalizacion de Proceso: \n")
        bot.sendMessage(chat_id, "Estado de Humedad: "+ESTADO_PLANTA)
        GPIO.output(pin_out,GPIO.HIGH)
    elif comando_upper =='SALIR':
       consultalog()
       bot.sendMessage(chat_id, "Adios")
    else:
       bot.sendMessage(chat_id, "Opcion invalida")
def Acceso():
    pin_in=16
    pin_in2=13
    pin_in3=15
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_in2,GPIO.IN)
    GPIO.setup(pin_in3,GPIO.IN)
    Ent1=GPIO.input(pin_in2)
    Ent2=GPIO.input(pin_in3)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_in,GPIO.IN)
    valor=GPIO.input(pin_in)
    txt3=open (filename3)
    lectura_Historico=txt3.read()
    Estado_pla="SECO"
    if   valor ==0: 
         Estado_pla='HUMEDO'
    else:
         Estado_pla='SECO'  
    if lectura_Historico=='True':
        if   valor ==1:
           Estado_pla="HUMEDO"
           GPIO.output(pin_out,GPIO.LOW)
           time.sleep(5)
           GPIO.output(pin_out,GPIO.HIGH)
        else:
           Estado_pla="SECO"
    if   Ent1 ==1 and Ent2==0:
      print("Tarjeta Correcta: ")
      Registrolog("CarlosP ",Estado_pla)
    elif Ent1 ==0 and Ent2==1:
      print("Token Correcto: ")
      Registrolog("CamilaG",Estado_pla)

def Cambio_Estado(Estado):
    csv=open (filename3,'w')
    csv.truncate(4)
    csv.write(Estado)
    csv.close
def consultalog():
    csv=open (filename)
    lectura=csv.read()
    print(lectura)
def creararchivo():
    csv=open (filename,'w')
    csv.write("Consultas\n")
    csv.close
def Registrolog(valor,valor2):
    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fecha_fin=str(fecha)
    dato="Fecha de Recoleccion: "+fecha_fin+" -- Ingreso: "+str(valor)+"--Estado del suelo: "+valor2+" --\n"
    csv=open (filename,'a')
    csv.write(dato)
    csv.close
    time.sleep(1)
try:
    archivo=open (filename).readable()
except:
    print("Creacion de archivo log")
    creararchivo()
     

bot = telepot.Bot('xxxxxx:AAHmtWpy8kgZQJtVawWwJrjUWZ_7xxxxxxxx')
bot.message_loop(handle)
print('Escuchando...')
while 1:
    Acceso()
    try:
        time.sleep(3)
    
    except KeyboardInterrupt:
        print('\n Programa detenido')
        GPIO.cleanup()
        exit()
    
    except:
        print('Other error or exception occured!')
        GPIO.cleanup()
