import json
import tiktoken
import time
import yaml
from config import GROQ_API_KEY, GROQ_MODELO
from datetime import datetime
from groq import Groq
from pathlib import Path

def registrar_log(resp, n_in: float, custo: float, t0: float, t1: float):
    registro = {
        "timestamp": datetime.now().isoformat(),
        "modelo": GROQ_MODELO,
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "total_tokens": resp.usage.total_tokens,
        "latencia_ms": round((t1 - t0) * 1000, 1),
        "saida": resp.choices[0].message.content,
        "prompt_tokens_tiktoken": n_in,
        "custo": f"USD {custo:.6f}"
    }

    registro_path = Path("logs/baseline_lab.json")
    registro_path.parent.mkdir(exist_ok=True)

    if registro_path.exists():
        with open(registro_path, encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []
    else:
        dados = []

    dados.append(registro)

    with open(registro_path, "w") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def custo_chamada(hist: list[dict], resp, preco_in=0.15, preco_out=0.60):
    n_in = 0
    enc = tiktoken.get_encoding("o200k_harmony")
    
    for msg in hist:
        n_in += 4 + len(enc.encode(msg["content"]))
    n_in += 2

    n_resp = resp.usage.completion_tokens

    custo = (n_in / 1000) * preco_in + (n_resp / 1000) * preco_out

    return n_in, n_resp, round(custo, 6)

def instanciar_cliente():
    client = Groq(
        api_key=GROQ_API_KEY,
    )
    return client


def chamar_modelo(msgs: list[dict]):
    client = instanciar_cliente()
    config_path = Path("configs/experimento-base.yaml")

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    ger = cfg["geracao"]
    temperatura = ger["temperatura"]
    modelo = GROQ_MODELO

    t0 = time.perf_counter()
    resp = client.chat.completions.create(
        model=modelo,
        messages=msgs,
        temperature=temperatura
    )
    t1 = time.perf_counter()

    return t0, t1, resp


