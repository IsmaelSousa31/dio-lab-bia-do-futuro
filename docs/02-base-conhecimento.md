# Base de Conhecimento

## Dados Utilizados

Nesta arquitetura avançada e híbrida, a base de conhecimento tradicional (dados em texto injetados no prompt) foi substituída por uma **Base de Regras Programáticas**. 

As regras de negócio do Departamento Pessoal não são enviadas para a IA ler, mas sim implementadas diretamente no motor matemático do Python.

| Arquivo/Módulo | Formato | Utilização no Agente |
|---------|---------|----------------------|
| `app.py` (Motor Matemático) | Função Python | Base de conhecimento algorítmica contendo as regras de cálculo, identificação de dias úteis via biblioteca `calendar` e regras de desconto de cada escala (5x2, 6x1 e 12x36). |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim. Os arquivos de dados mockados originais do template (CSV, JSON) foram removidos.
Foi constatado durante os testes que enviar regras de cálculo matemático (como o antigo `base.json`) para o *System Prompt* fazia com que o LLM sofresse de "alucinação" ao tentar adivinhar o calendário oficial e deduzir feriados. 

Para resolver isto, os dados e regras foram **adaptados de texto para código algorítmico**. A base de conhecimento do agente agora reside na lógica da função `calcular_todas_escalas`, garantindo 100% de precisão matemática, sem depender da probabilidade de geração de texto da IA.

---

## Estratégia de Integração

### Como os dados são carregados e processados?
> Descreva como seu agente acessa a base de conhecimento.

A estratégia de integração foi dividida em dois motores independentes (Arquitetura Híbrida):

1. **O LLM (Extrator):** O utilizador interage com o agente enviando uma string padronizada (ex: `03 - 2026 - 25 - 17, 18 - 0`). O LLM atua APENAS como um tradutor, extraindo as intenções e transformando essa entrada num objeto JSON limpo e estruturado.
2. **O Motor Python (A Base de Conhecimento Viva):** O Python recebe o JSON da IA, cruza a data com a biblioteca nativa `calendar` e aplica as regras de negócio intrínsecas ao código (ex: ignorar domingos na escala 6x1, não descontar feriados no 12x36). 

**Exemplo do Motor de Regras (Base de Conhecimento Aplicada):**
```python
# Lógica da Escala 12x36 integrada diretamente no processamento
if dia % 2 != 0:
    dias_12x36_impar += 1 # Não desconta feriados, conforme regra do DP
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

As regras de cálculo **não vão no system prompt**. O *System Prompt* agora é utilizado exclusivamente para forçar a IA a respeitar o formato de extração, impedindo *prompt injection* e garantindo que ela não tente calcular nada por conta própria.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

Como o cálculo foi delegado ao Python, o **System Prompt** foca-se apenas na extração segura de dados e roteamento das interações. Abaixo está o contexto real de como o LLM é instruído:

```text
Você é uma API de roteamento de dados. 
Sua ÚNICA função é classificar a entrada do usuário e retornar EXATAMENTE UMA das 3 opções abaixo:

OPÇÃO 1: Se o usuário enviou os dados matemáticos separados por hífen, retorne APENAS o JSON.
Exemplo: 03 - 2026 - 25 - 17, 18 - 0
Retorno:
{
  "mes": 3, "ano": 2026, "valor": 25.0, "feriados": [17, 18], "faltas": 0
}

OPÇÃO 2: Se o usuário enviou APENAS um cumprimento (ex: "oi", "olá", "bom dia") ou pediu ajuda, retorne EXATAMENTE a
