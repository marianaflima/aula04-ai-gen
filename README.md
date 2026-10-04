# aula04-ai-gen

> **Disciplina:** IA Generativa — FACAPE
> **Aluno(a):** Mariana Félix de Lima
> **Professor(a):** Mateus Amorim
> **Atividade:** Laboratório de baseline de geração com LLMs (LabIA)

Projeto desenvolvido como tarefa da disciplina de IA Generativa. É um **laboratório de baseline**
que chama modelos da **Groq**, mede **latência**, **tokens** e **custo estimado** de cada chamada,
e registra tudo em log JSON para análise posterior.

## 📁 Estrutura do projeto

```text
aula04-ai-gen/
├── configs/
│   └── experimento-base.yaml   # Parâmetros do experimento (temperatura, seeds, tarefas)
├── logs/
│   └── baseline_lab.json       # Registro de cada chamada (append)
├── main.py                     # Executa o laço de teste (3 iterações)
├── baseline_lab.py             # Núcleo: chamada, custo e log
├── config.py                   # Carrega .env (GROQ_API_KEY, GROQ_MODELO)
├── check_env.py                # Verifica se o ambiente está pronto
├── requirements.txt            # Dependências (freeze)
├── pyproject.toml              # Metadados do projeto (Python >= 3.12)
├── .env.example                # Modelo de variáveis de ambiente
└── .gitignore
```

## 🧰 Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Chave de API da [Groq](https://console.groq.com/)

## ⚙️ Instalação

Usamos `uv` para gerenciar as dependências:

```bash
uv pip install -r requirements.txt
```

## 🔑 Configuração

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=sua-chave-aqui
GROQ_MODELO=openai/gpt-oss-20b
```

> ⚠️ O `.env` é ignorado pelo Git — nunca suba sua chave para o repositório.

## 🚀 Quickstart

```bash
# 1. Verifica se o ambiente está pronto
python3 check_env.py

# 2. Roda o experimento baseline
python3 main.py
```

### Exemplo de saída

```text
Modelo GROQ: openai/gpt-oss-20b (chave carregada: OK)
============================================================
Inicialização do programa
============================================================
1ª iteracao de teste    [OK]
2ª iteracao de teste    [OK]
3ª iteracao de teste    [OK]
============================================================
Finalização do programa
============================================================
```

## 🧩 Como funciona

O núcleo está em `baseline_lab.py`, com três funções:

| Função | Responsabilidade |
|---|---|
| `chamar_modelo(msgs)` | Instancia o cliente Groq, lê a **temperatura** de `configs/experimento-base.yaml` e faz a chamada medindo o tempo com `time.perf_counter()` |
| `custo_chamada(hist, resp)` | Conta os tokens do histórico com `tiktoken` (encoding `o200k_harmony`) e estima o custo em USD |
| `registrar_log(...)` | Grava em `logs/baseline_lab.json` timestamp, modelo, tokens, latência, saída e custo |

### Cálculo de custo

O cálculo de custo foi estabelecido seguindo a fórmula proposta em sala de aula:

```text
custo = (tokens_entrada / 1000) × preço_entrada + (tokens_saída / 1000) × preço_saída
```

Com os preços padrão de `preco_in=0.15` e `preco_out=0.60`, que podem ser
alterados na chamada de `custo_chamada()`. A contagem de tokens de entrada
considera `+4` tokens por mensagem e `+2` tokens fixos, conforme a fórmula
da aula.

## 📄 Formato do log

Cada chamada gera um registro em `logs/baseline_lab.json`:

| Campo | Descrição |
|---|---|
| `timestamp` | Data/hora ISO 8601 da chamada |
| `modelo` | Modelo utilizado (ex.: `openai/gpt-oss-20b`) |
| `prompt_tokens` | Tokens de entrada (reportado pela API) |
| `completion_tokens` | Tokens de saída (reportado pela API) |
| `total_tokens` | Total de tokens da chamada |
| `latencia_ms` | Latência da chamada em milissegundos |
| `saida` | Texto completo gerado pelo modelo |
| `prompt_tokens_tiktoken` | Tokens de entrada contados localmente com `tiktoken` |
| `custo` | Custo estimado em USD |

### Exemplo de registro

```json
{
  "timestamp": "2026-10-03T12:33:36.274556",
  "modelo": "openai/gpt-oss-20b",
  "prompt_tokens": 100,
  "completion_tokens": 136,
  "total_tokens": 236,
  "latencia_ms": 1045.8,
  "saida": "RAG (Retrieval-Augmented Generation) é uma técnica de IA que combina a busca de documentos relevantes em um banco de dados com a geração de texto...",
  "prompt_tokens_tiktoken": 36,
  "custo": "USD 0.087000"
}
```

## 🔬 Experimento base

Os parâmetros ficam em `configs/experimento-base.yaml`:

```yaml
geracao:
  temperatura: 0.2
  top_p: 0.9
  max_tokens_resposta: 512
```

Hoje, a baseline consome o campo **`temperatura`** — é ele que controla a
criatividade/respostas do modelo a cada chamada.

### Como criar novos experimentos

Basta acessar `configs/experimento-base.yaml` e ajustar conforme necessário

Dica: rode duas vezes com temperaturas diferentes e compare o campo `saida`
dos registros em `logs/baseline_lab.json`.


## Uso de IA
Deixo registrado que utilizei IA para fins de analisar o projeto e gerar essa documentação do README, al. 

