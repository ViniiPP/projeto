# button.py
import RPi.GPIO as GPIO
import requests
from time import sleep

pushbutton_pin = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pushbutton_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def send_post_request():
    data = {'message': 'Botão pressionado'}
    try:
        response = requests.post('http://localhost:5000/logs', json=data)
        if response.status_code == 201:
            print("Log enviado com sucesso!")
        else:
            print(f"Erro ao enviar log: {response.status_code}")
    except Exception as e:
        print(f"Erro na conexão: {e}")

if __name__ == "__main__":
    result = int(input("1-Executar método\n2-Iniciar aplicação\nEscolha: "))
    
    if result == 1:
        send_post_request()
    else:
        try:
            while True:
                if GPIO.input(pushbutton_pin) == GPIO.HIGH:
                    print("Botão pressionado")
                    send_post_request()
                    sleep(0.5)
        except KeyboardInterrupt:
            print("Programa interrompido")
        finally:
            GPIO.cleanup()
