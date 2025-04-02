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
 