import json
import os

# --- ARQUIVOS UTILIZADOS ---
ARQUIVO_TXT = "registros_colonia.txt"
ARQUIVO_JSON = "dados_colonia.json"

# --- JUSTIFICATIVA DE ARMAZENAMENTO ---
# .txt: Utilizado para logs contínuos, registros de auditoria e texto não estruturado (operações com append 'a').
# .json: Utilizado para dados estruturados (módulos, alertas e modelos de prompts) facilitando chave-valor.

def salvar_em_txt(mensagem):
    """Grava logs e ocorrências técnicas no arquivo de texto."""
    with open(ARQUIVO_TXT, mode="a", encoding="utf-8") as f:
        f.write(f"{mensagem}\n")
    print(f"[LOG GERADO]: Registrado em {ARQUIVO_TXT}")

def carregar_dados_json():
    """Carrega dados estruturados do arquivo JSON."""
    if not os.path.exists(ARQUIVO_JSON):
        print(f"Erro: Arquivo {ARQUIVO_JSON} não encontrado.")
        return None
    with open(ARQUIVO_JSON, mode="r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados_json(dados):
    """Salva dados estruturados atualizados no arquivo JSON."""
    with open(ARQUIVO_JSON, mode="w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"[SUCESSO]: Dados salvos em {ARQUIVO_JSON}")

def avaliar_regra_logica(falha, critico):
    """
    Avaliação Lógica do Alerta
    Regra Original: ALERTA = (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO)
    Regra Simplificada: ALERTA = FALHA
    """
    alerta_original = (falha and critico) or (falha and not critico)
    alerta_simplificado = falha
    
    # Validação da igualdade entre a expressão complexa e a simplificada
    assert alerta_original == alerta_simplificado
    return alerta_simplificado

def menu_cadastrar_registro():
    print("\n--- CADASTRAR REGISTRO TÉCNICO DE CAMPO ---")
    modulo = input("Nome do Módulo (ex: Suporte de Vida, Energia): ")
    descricao = input("Descrição da Ocorrência: ")
    registro = f"MODULO: {modulo} | OCORRÊNCIA: {descricao}"
    salvar_em_txt(registro)

def menu_consultar_registros():
    print("\n--- CONSULTAR REGISTROS (TXT) ---")
    if not os.path.exists(ARQUIVO_TXT):
        print("Nenhum registro encontrado.")
        return
    with open(ARQUIVO_TXT, mode="r", encoding="utf-8") as f:
        conteudo = f.read()
        print(conteudo if conteudo else "O arquivo de texto está vazio.")

def menu_analisar_alerta_e_simular_ia():
    print("\n--- ANÁLISE DE ALERTA OPERACIONAL E SIMULAÇÃO DE IA ---")
    dados = carregar_dados_json()
    if not dados:
        return

    alertas = dados.get("alertas", [])
    if not alertas:
        print("Nenhum alerta disponível para análise.")
        return

    print("Alertas disponíveis:")
    for idx, alt in enumerate(alertas):
        print(f"{idx + 1}. Módulo: {alt['modulo']} | Falha: {alt['falha']} | Crítico: {alt['critico']}")

    try:
        opcao = int(input("Selecione o número do alerta para processar: ")) - 1
    except ValueError:
        print("Entrada inválida.")
        return

    if 0 <= opcao < len(alertas):
        alerta_sel = alertas[opcao]
        
        # Executando validação lógica booleana
        emite_alerta = avaliar_regra_logica(alerta_sel["falha"], alerta_sel["critico"])
        
        print("\n[PROCESSANDO REGRA DE DECISÃO BOOLEANA]")
        print("Expressão: (FALHA AND CRITICO) OR (FALHA AND NOT CRITICO) ==> Simplificada para: FALHA")
        print(f"Resultado da Avaliação: Emite Alerta? {emite_alerta}")

        if emite_alerta:
            print("\n--- GERANDO PROMPT E RESPOSTA DA IA ---")
            prompt_template = dados["prompts"]["resumo_alerta"]
            
            # Formatando o prompt estruturado (Few-shot/Structured Output)
            prompt_formatado = f"{prompt_template['instrucao']}\nExemplo: {prompt_template['exemplo']}\nEntrada: {alerta_sel}"
            print(f"\n[PROMPT ESTRUTURADO ENVIADO AO MODELO]:\n{prompt_formatado}")

            # Simulação do Assistente Inteligente
            resposta_simulada = {
                "status_alerta": "CRÍTICO" if alerta_sel["critico"] else "ATENÇÃO",
                "modulo_afetado": alerta_sel["modulo"],
                "mensagem_curta": alerta_sel["mensagem"],
                "acao_recomendada": "Deslocar equipe técnica imediatamente." if alerta_sel["critico"] else "Monitorar consumo em tempo real."
            }
            
            print("\n[RESPOSTA SIMULADA DO ASSISTENTE (JSON / STRUCTURED OUTPUT)]:")
            print(json.dumps(resposta_simulada, indent=4, ensure_ascii=False))
            
            # Salvar interação nos históricos
            dados["historico_interacoes"].append({
                "prompt": prompt_formatado,
                "resposta": resposta_simulada
            })
            salvar_dados_json(dados)
    else:
        print("Opção inválida.")

def menu_exibir_prompts():
    dados = carregar_dados_json()
    if dados and "prompts" in dados:
        print("\n--- MODELOS DE PROMPTS CADASTRADOS ---")
        print(json.dumps(dados["prompts"], indent=4, ensure_ascii=False))

def menu_principal():
    while True:
        print("\n==========================================")
        print("  NÚCLEO COGNITIVO DA AURORA SIGER (NCAS)")
        print("==========================================")
        print("1. Cadastrar registro técnico da colônia (.txt)")
        print("2. Consultar registros técnicos (.txt)")
        print("3. Analisar alerta operacional, validar lógica e simular IA (.json)")
        print("4. Exibir Prompts Estruturados")
        print("5. Sair")
        
        opcao = input("Escolha uma opção (1-5): ")
        
        if opcao == "1":
            menu_cadastrar_registro()
        elif opcao == "2":
            menu_consultar_registros()
        elif opcao == "3":
            menu_analisar_alerta_e_simular_ia()
        elif opcao == "4":
            menu_exibir_prompts()
        elif opcao == "5":
            print("Encerrando o sistema NCAS...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
