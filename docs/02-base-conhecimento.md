# Base de Conhecimento

## Dados Utilizados



| Arquivo | Formato | Utilização no Agente |
|---------|---------|----------------------|
| `base.json` | JSON | Base de conhecimento contendo as regras de cálculo, escalas de trabalho e parâmetros de feriados |


> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim. Os arquivos de dados mockados originais do template foram removidos. Foi mantido e adaptado exclusivamente o arquivo `base.json`, que foi estruturado sob medida para armazenar a base de conhecimento do agente, contendo as regras de cálculo de vale-alimentação, os tipos de escalas de trabalho e os parâmetros para tratamento de feriados.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

O arquivo `base.json` é carregado no início da execução da aplicação através de um script em Python. Os dados são lidos da pasta `data`, convertidos em um dicionário (dictionary) e, em seguida, formatados e injetados no contexto do *System Prompt* do agente, garantindo que ele tenha acesso a todas as regras de cálculo e escalas de trabalho antes de iniciar a interação com o usuário.

**Código de carregamento:**

```python
import json
import os

def carregar_base_conhecimento():
    # Caminho para o arquivo base.json dentro da pasta data
    caminho_arquivo = os.path.join("data", "base.json")
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            base_conhecimento = json.load(arquivo)
            return base_conhecimento
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print("Erro: Falha ao decodificar o arquivo JSON.")
        return None

# Executando o carregamento
dados_agente = carregar_base_conhecimento()

if dados_agente:
    print("Base de conhecimento carregada com sucesso!")
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados extraídos do arquivo `base.json` são injetados diretamente no **System Prompt** (prompt de sistema) do agente logo na inicialização da conversa. 

Como o arquivo contém as regras de negócio fixas da empresa (a fórmula de cálculo e as definições exatas das escalas de trabalho, como 5x2 ou 12x36), enviar essas informações como contexto base garante que o **CalculadorIA** compreenda as políticas do Departamento Pessoal de forma estrita. Assim, quando o usuário fornece as variáveis dinâmicas no chat (qual é o mês, se há feriados e o valor diário do vale), o agente cruza essas entradas em tempo real com as regras já consolidadas em seu prompt de sistema, realizando o cálculo de forma precisa e sem alucinar.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

Após o script Python ler o arquivo `base.json`, os dados são formatados em texto claro e concatenados com as instruções de comportamento do agente, formando o **System Prompt**. Abaixo está um exemplo de como o LLM recebe esse contexto:

```text
Você é o CalculadorIA, um assistente virtual formal e objetivo que atua no Departamento Pessoal.
Sua função exclusiva é calcular o total de vales-alimentação dos funcionários de forma precisa.

=== BASE DE CONHECIMENTO E REGRAS ===
Fórmula Base: (Dias Trabalhados no Mês - Feriados Não Trabalhados) * Valor Diário

Escalas de Trabalho Permitidas:
1. Escala: 5x2
   - Descrição: Trabalha 5 dias e folga 2 dias consecutivos.
   - Trabalha em feriados: Não
   - Desconta feriado do vale: Sim

2. Escala: 6x1
   - Descrição: Trabalha 6 dias e folga 1 dia.
   - Trabalha em feriados: Não
   - Desconta feriado do vale: Sim

3. Escala: 12x36
   - Descrição: Trabalha 12 horas seguidas e descansa 36 horas.
   - Trabalha em feriados: Sim
   - Desconta feriado do vale: Não

=== INSTRUÇÕES DE OPERAÇÃO ===
1. Colete com o usuário: Mês base, quantidade de feriados no mês, valor do vale por dia e a escala do funcionário.
2. Realize o cálculo passo a passo, demonstrando a matemática na resposta.
3. Se o usuário perguntar sobre assuntos fora do cálculo de benefícios, responda formalmente que você não possui essa informação.
4. Nunca presuma feriados regionais; utilize apenas os dados fornecidos pelo usuário.
