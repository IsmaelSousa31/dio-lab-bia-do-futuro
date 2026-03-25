# 🧮 CalculadorIA - Agente Inteligente para Departamento Pessoal

## Contexto

Os assistentes virtuais no setor de Recursos Humanos e Departamento Pessoal estão a evoluir de simples chatbots reativos para **sistemas especialistas inteligentes**. Neste desafio, idealizamos e prototipámos um agente de DP que utiliza IA Generativa integrada a lógicas matemáticas exatas para:

- **Automatizar cálculos complexos** de benefícios (vale-alimentação) com precisão absoluta.
- **Processar múltiplas escalas de trabalho** (5x2, 6x1, 12x36) de forma simultânea.
- **Garantir segurança** e confiabilidade nas respostas, adotando uma arquitetura híbrida (anti-alucinação) onde a IA atua na extração de dados e o código nativo resolve a matemática.

---

## O Que Foi Entregue Neste Projeto

### 1. Documentação do Agente

Definição de **o que** o agente faz e **como** ele funciona:

- **Caso de Uso:** Resolução do cálculo automatizado de vales-alimentação, considerando as particularidades de cada escala.
- **Persona e Tom de Voz:** Formal, direto e objetivo, focado na rotina do analista de DP.
- **Arquitetura:** Fluxo de injeção de prompt e interceção via Python.
- **Segurança:** Trava contra Injeção de Prompt (Hack) e delegação da matemática para bibliotecas nativas para evitar alucinação numérica.

📄 **Documentação:** [`docs/01-documentacao-agente.md`](./docs/01-documentacao-agente.md)

---

### 2. Base de Conhecimento

Utilização de uma base de regras customizada em formato JSON para alimentar as lógicas do agente:

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `base.json` | JSON | Base de conhecimento contendo as regras de cálculo e as características de cada escala (ex: descontar feriado ou não). |

📄 **Documentação:** [`docs/02-base-conhecimento.md`](./docs/02-base-conhecimento.md)

---

### 3. Prompts do Agente

Documentação da engenharia de prompts que define o comportamento do agente:

- **System Prompt:** Instruções restritas que obrigam o agente a atuar apenas como classificador e extrator de JSON.
- **Tratamento de Edge Cases:** Como o agente se comporta em caso de saudações ("Oi", "Bom dia") ou pedidos fora do contexto (ex: "Me dê um código de programação").

📄 **Documentação:** [`docs/03-prompts.md`](./docs/03-prompts.md)

---

### 4. Aplicação Funcional

Um **protótipo funcional** do agente híbrido:

- Interface de chat desenvolvida com **Streamlit**.
- Integração de IA utilizando o modelo **Llama-3.1-8b-instant** através da API da **Groq**.
- Motor matemático infalível construído com a biblioteca `calendar` do Python.

📁 **Código e Execução:** [`src/`](./src/)

---

### 5. Avaliação e Métricas

Testes de garantia de qualidade (QA) aplicados ao agente:

- Testes de Injeção de Prompt (Jailbreak).
- Testes com entradas incompletas ou mal formatadas.
- Testes de estresse com cenários de cálculo válidos para validação da "armadura" do sistema.

📄 **Documentação:** [`docs/04-metricas.md`](./docs/04-metricas.md)

---

## Ferramentas Utilizadas

| Categoria | Ferramentas |
|-----------|-------------|
| **LLMs / IA** | API da [Groq](https://groq.com/) (Modelo Llama 3) |
| **Desenvolvimento** | [Python](https://www.python.org/), [Streamlit](https://streamlit.io/) |
| **Manipulação de Datas** | Bibliotecas nativas `calendar` e `datetime` |

---

## Estrutura do Repositório

```text
📁 lab-agente-financeiro/
│
├── 📄 README.md                      # Esta documentação principal do desafio
│
├── 📁 data/                          # Dados e Regras de Negócio
│   └── base.json                     # Regras das escalas (JSON)
│
├── 📁 docs/                          # Documentação detalhada do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md       # Estratégia de dados e integração
│   ├── 03-prompts.md                 # Engenharia de prompts e Few-Shot
│   └── 04-metricas.md                # Avaliação e testes de stress
│
├── 📁 src/                           # Código da aplicação
│   ├── app.py                        # Motor do Chatbot (Streamlit + Groq + Python)
│   └── README.md                     # Guia de instalação e execução
│
└── 📁 assets/                        # Imagens e diagramas
    └── ...
```
