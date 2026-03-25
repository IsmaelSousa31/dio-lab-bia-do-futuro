# 🧮 CalculadorIA - Sistema Inteligente para Departamento Pessoal

Este projeto é um assistente virtual construído com Python, Streamlit e Inteligência Artificial (Groq API / Llama 3) focado em automatizar o cálculo de vale-alimentação para múltiplas escalas de trabalho (5x2, 6x1 e 12x36).

## 🚀 O Problema e a Solução Arquitetural
Modelos de Linguagem (LLMs) costumam sofrer de "alucinações matemáticas" ao tentar processar calendários e contar dias úteis. Para garantir **100% de precisão**, este sistema adota uma arquitetura híbrida:
1. **O Chat Inteligente (IA):** Atua exclusivamente como um extrator de dados, lendo a entrada do usuário e convertendo em um objeto JSON estruturado.
2. **O Motor Matemático (Python):** Recebe o JSON, utiliza a biblioteca nativa `calendar` para mapear os dias do mês exatos e aplica as regras de negócio de descontos e feriados de forma infalível.

## 📂 Estrutura do Projeto

```text
src/
├── app.py              # Aplicação principal (Interface Streamlit + Lógica + Integração Groq)
└── requirements.txt    # Dependências do projeto
```

## 🛠️ Tecnologias Utilizadas

Para este projeto, utilizamos o Streamlit para a interface web e a biblioteca da Groq para a comunicação super-rápida com o modelo Llama 3. O arquivo `requirements.txt` contém:

```text
streamlit
groq
```

## ⚙️ Como Configurar e Rodar Localmente

1. **Adicione sua chave de API:**
   Abra o arquivo `src/app.py` e substitua `"sua_chave_api_aqui"` pela sua chave real gerada no [Groq Console](https://console.groq.com/).

2. **Instale as dependências:**
   No terminal, execute o comando abaixo para instalar as bibliotecas necessárias:
   ```bash
   pip install -r src/requirements.txt
   ```

3. **Inicie a aplicação:**
   Ainda no terminal, rode o Streamlit:
   ```bash
   streamlit run src/app.py
   ```

## 💡 Como Usar o Chat

A IA foi treinada para receber os dados em um formato ágil e otimizado para a rotina de DP. No chat da aplicação, envie os dados separados por hífen (`-`):

**Formato exigido:** `Mês - Ano - Valor - Feriados - Faltas`

**Exemplos de uso:**
* Com feriados: `03 - 2026 - 25 - 17, 18 - 0`
* Sem feriados: `04 - 2026 - 30 - nenhum - 1`

O sistema irá gerar um relatório completo calculando os valores para as equipes 5x2, 6x1 e 12x36 (Ímpar e Par) simultaneamente! Para realizar um novo cálculo, basta digitar `R` no chat.
