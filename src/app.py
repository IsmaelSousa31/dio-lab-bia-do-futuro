import json
import calendar
import datetime
import streamlit as st
from groq import Groq

# =========== CONFIGURAÇÃO DA NUVEM ===========
CHAVE_API = "sua_chave_api_aqui"  # Insira sua chave da Groq
cliente = Groq(api_key=CHAVE_API)
MODELO = "llama-3.1-8b-instant"

# =========== 1. MOTOR MATEMÁTICO ===========
def calcular_todas_escalas(ano, mes_num, valor_diario, lista_feriados, faltas):
    _, total_dias = calendar.monthrange(ano, mes_num)
    
    dias_5x2 = 0
    dias_6x1 = 0
    dias_12x36_impar = 0
    dias_12x36_par = 0

    for dia in range(1, total_dias + 1):
        dia_semana = datetime.date(ano, mes_num, dia).weekday() # 0=Seg, 6=Dom

        if dia_semana <= 4 and dia not in lista_feriados:
            dias_5x2 += 1
        if dia_semana <= 5 and dia not in lista_feriados:
            dias_6x1 += 1
        if dia % 2 != 0:
            dias_12x36_impar += 1
        if dia % 2 == 0:
            dias_12x36_par += 1

    res_5x2 = {"dias": max(0, dias_5x2 - faltas), "valor": max(0, dias_5x2 - faltas) * valor_diario}
    res_6x1 = {"dias": max(0, dias_6x1 - faltas), "valor": max(0, dias_6x1 - faltas) * valor_diario}
    res_impar = {"dias": max(0, dias_12x36_impar - faltas), "valor": max(0, dias_12x36_impar - faltas) * valor_diario}
    res_par = {"dias": max(0, dias_12x36_par - faltas), "valor": max(0, dias_12x36_par - faltas) * valor_diario}

    return res_5x2, res_6x1, res_impar, res_par

# =========== 2. MENSAGENS PADRÃO E CÉREBRO DA IA ===========
MENSAGEM_INSTRUCOES = """Para um cálculo super rápido de todas as escalas, envie os dados separados por hífen (`-`), nesta ordem exata:

**Mês - Ano - Valor do Vale - Feriados - Faltas**

*Exemplo:*
`03 - 2026 - 25 - 17, 18 - 0`
*(Referente a: Março - 2026 - R$ 25,00 - Feriados dias 17 e 18 - Zero faltas)*"""

MENSAGEM_ERRO = f"Desculpe, não compreendi. Vamos tentar novamente:\n\n{MENSAGEM_INSTRUCOES}"

SYSTEM_PROMPT = """Você é uma API de roteamento de dados. 
Sua ÚNICA função é classificar a entrada do usuário e retornar EXATAMENTE UMA das 3 opções abaixo:

OPÇÃO 1: Se o usuário enviou os dados matemáticos separados por hífen, retorne APENAS o JSON.
Exemplo: 03 - 2026 - 25 - 17, 18 - 0
Retorno:
{
  "mes": 3, "ano": 2026, "valor": 25.0, "feriados": [17, 18], "faltas": 0
}

OPÇÃO 2: Se o usuário enviou APENAS um cumprimento (ex: "oi", "olá", "bom dia") ou pediu ajuda, retorne EXATAMENTE a palavra: INSTRUCOES

OPÇÃO 3: Se o usuário enviou um formato inválido, dados incompletos ou pediu códigos de programação, retorne EXATAMENTE a palavra: ERRO
"""

# =========== 3. INTEGRAÇÃO CHAT <-> PYTHON ===========
st.set_page_config(page_title="CalculadorIA DP", page_icon="🧮")
st.title("🧮 CalculadorIA - Relatório Geral")

if pergunta := st.chat_input("Ex: 03 - 2026 - 25 - 17, 18 - 0 ou digite R para reiniciar"):
    st.chat_message("user").write(pergunta)
    
    # Se o usuário digitar "R" ou "r", o Python já reinicia na hora sem gastar a IA
    if pergunta.strip().upper() == "R":
        st.chat_message("assistant").write(f"🔄 Tudo pronto para um novo cálculo!\n\n{MENSAGEM_INSTRUCOES}")
    
    else:
        with st.spinner("Processando..."):
            try:
                resposta = cliente.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": pergunta}
                    ],
                    model=MODELO,
                    temperature=0.0 
                )
                
                conteudo_ia = resposta.choices[0].message.content.strip()
                conteudo_ia = conteudo_ia.replace("```json", "").replace("```", "").strip()

                # CAMINHO 1: A IA identificou que é um cálculo válido
                if conteudo_ia.startswith("{") and conteudo_ia.endswith("}"):
                    dados = json.loads(conteudo_ia)
                    
                    r_5x2, r_6x1, r_impar, r_par = calcular_todas_escalas(
                        dados['ano'], dados['mes'], dados['valor'], 
                        dados['feriados'], dados['faltas']
                    )
                    
                    meses_nomes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
                    nome_mes = meses_nomes[dados['mes']-1]
                    feriados_texto = ", ".join(map(str, dados['feriados'])) if dados['feriados'] else "Nenhum"
                    
                    resposta_final = f"""✅ **Relatório de Cálculo - Todas as Escalas**
                    
**Mês de Referência:** {nome_mes}/{dados['ano']}
**Feriados / Fechamentos:** {feriados_texto}
**Faltas descontadas:** {dados['faltas']}

---
🏢 **Escala 5x2 (Segunda a Sexta)**
▶ Trabalhará: {r_5x2['dias']} dias | **Receberá: R$ {r_5x2['valor']:.2f}**

🏪 **Escala 6x1 (Segunda a Sábado)**
▶ Trabalhará: {r_6x1['dias']} dias | **Receberá: R$ {r_6x1['valor']:.2f}**

🚑 **Escala 12x36 (Início em Dia Ímpar)** *(Dias 1, 3, 5...)*
▶ Trabalhará: {r_impar['dias']} dias | **Receberá: R$ {r_impar['valor']:.2f}**

🚑 **Escala 12x36 (Início em Dia Par)** *(Dias 2, 4, 6...)*
▶ Trabalhará: {r_par['dias']} dias | **Receberá: R$ {r_par['valor']:.2f}**

---
🔄 **Digite R para iniciarmos novamente.**
""".replace('.', ',')
                    
                    st.chat_message("assistant").write(resposta_final)
                
                # CAMINHO 2: A IA identificou que foi só um "Oi" ou "Bom dia"
                elif conteudo_ia == "INSTRUCOES":
                    st.chat_message("assistant").write(f"Olá! Tudo bem? 👋\n\n{MENSAGEM_INSTRUCOES}")
                
                # CAMINHO 3: A IA identificou que o texto estava errado ou malicioso
                else:
                    st.chat_message("assistant").write(MENSAGEM_ERRO)

            except Exception as e:
                st.chat_message("assistant").write(MENSAGEM_ERRO)
