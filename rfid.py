# rfid.py
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import requests
from datetime import datetime

class SistemaControleAcesso:
    def __init__(self):
        # Pinos de LED e buzzer (exemplo)
        self.GREEN_LED = 17
        self.RED_LED = 27
        self.BUZZER = 22  # Ajuste conforme seu hardware

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GREEN_LED, GPIO.OUT)
        GPIO.setup(self.RED_LED, GPIO.OUT)
        GPIO.setup(self.BUZZER, GPIO.OUT)

        self.leitorRfid = SimpleMFRC522()

        # Mapeia quem está dentro ou fora, por exemplo
        self.estado_colaboradores = {}  # {tag: "inside"/"outside"}

    def send_log_to_api(self, message):
        """Envia log pra nossa API Flask, que salva no DB e publica no PubNub."""
        try:
            url = "http://localhost:5000/logs"
            data = {"message": message}
            resp = requests.post(url, json=data)
            if resp.status_code == 201:
                print("Log enviado com sucesso:", message)
            else:
                print("Erro ao enviar log:", resp.status_code, resp.text)
        except Exception as e:
            print("Erro na conexão com API:", e)

    def tocar_buzzer(self, tempo=0.2, freq=500):
        """Toca o buzzer por um tempo/frequência específicos (exemplo simples)."""
        GPIO.output(self.BUZZER, GPIO.HIGH)
        time.sleep(tempo)
        GPIO.output(self.BUZZER, GPIO.LOW)

    def process_tag(self, tag):
        """Verifica se a tag está autorizada, se é entrada ou saída, etc."""
        # Aqui, em vez de ter um 'cadastro' fixo, podemos consultar a API
        # ou o DB pra saber se essa tag existe e está autorizada.
        # Pra simplificar, vamos só fazer um GET local (ou suposição).
        # Exemplo: chame /collaborators ou algo assim. Vou supor que já existe e é autorizado.

        # Exemplo bobo: se a tag for 123456, vamos dizer que é do "Fulano" e é autorizado.
        # Ajuste para buscar do DB de verdade!
        if tag == 123456:
            nome = "Fulano"
            autorizado = True
        else:
            nome = "Desconhecido"
            autorizado = False

        if not autorizado:
            # Registro de tentativa não autorizada
            GPIO.output(self.RED_LED, GPIO.HIGH)
            self.tocar_buzzer(tempo=0.5, freq=300)
            GPIO.output(self.RED_LED, GPIO.LOW)

            self.send_log_to_api(f"Tentativa NÃO AUTORIZADA para tag {tag} - {datetime.now()}")
            return

        # Se autorizado, verificar se é entrada ou saída
        estado_atual = self.estado_colaboradores.get(tag, "outside")

        if estado_atual == "outside":
            # Entrando
            self.estado_colaboradores[tag] = "inside"
            GPIO.output(self.GREEN_LED, GPIO.HIGH)
            self.tocar_buzzer(tempo=0.2, freq=1000)
            GPIO.output(self.GREEN_LED, GPIO.LOW)

            self.send_log_to_api(f"{nome} (tag {tag}) entrou às {datetime.now()}")

        else:
            # Saindo
            self.estado_colaboradores[tag] = "outside"
            GPIO.output(self.GREEN_LED, GPIO.HIGH)
            self.tocar_buzzer(tempo=0.1, freq=2000)
            GPIO.output(self.GREEN_LED, GPIO.LOW)

            self.send_log_to_api(f"{nome} (tag {tag}) saiu às {datetime.now()}")

    def iniciar(self):
        try:
            print("Sistema de Controle de Acesso Iniciado. Aguardando leituras...")
            while True:
                tag, text = self.leitorRfid.read()
                self.process_tag(tag)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando sistema RFID...")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    sistema = SistemaControleAcesso()
    sistema.iniciar()
