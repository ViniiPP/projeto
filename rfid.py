# rfid.py
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
import requests
from datetime import datetime

class SistemaControleAcesso:
    def __init__(self):
        # Inicialização do leitor RFID
        self.leitorRfid = SimpleMFRC522()

        # Mapeia o estado dos colaboradores (dentro ou fora)
        self.estado_colaboradores = {}  # {tag: "inside"/"outside"}

    def send_log_to_api(self, message):
        """Envia log para a API Flask, que salva no DB e publica no PubNub."""
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

    def process_tag(self, tag):
        """Verifica se a tag está autorizada consultando os colaboradores e registra entrada/saída."""
        url = "http://localhost:5000/collaborators"
        try:
            response = requests.get(url)
            colaboradores = response.json()
        except Exception as e:
            print("Erro ao buscar colaboradores:", e)
            return

        # Inicialmente, define como desconhecido e não autorizado
        nome = "Desconhecido"
        autorizado = False

        # Faz um loop pelos colaboradores para ver se a tag corresponde
        for colaborador in colaboradores:
            if colaborador.get("tag") == tag:
                nome = colaborador.get("name", "Desconhecido")
                autorizado = colaborador.get("authorized", False)
                break

        # Se não estiver autorizado, envia log de tentativa não autorizada
        if not autorizado:
            self.send_log_to_api(f"Tentativa NÃO AUTORIZADA para tag {tag} - {datetime.now()}")
            return

        # Verifica se o colaborador está entrando ou saindo
        estado_atual = self.estado_colaboradores.get(tag, "outside")
        if estado_atual == "outside":
            self.estado_colaboradores[tag] = "inside"
            self.send_log_to_api(f"{nome} (tag {tag}) entrou às {datetime.now()}")
        else:
            self.estado_colaboradores[tag] = "outside"
            self.send_log_to_api(f"{nome} (tag {tag}) saiu às {datetime.now()}")
 

    def iniciar(self):
        try:
            print("Sistema de Controle de Acesso Iniciado. Aguardando leituras...")
            while True:
                tag, _ = self.leitorRfid.read()
                self.process_tag(tag)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando sistema RFID...")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    sistema = SistemaControleAcesso()
    sistema.iniciar()
 