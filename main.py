import check_env
import yaml
from baseline_lab import chamar_modelo, custo_chamada, registrar_log
from pathlib import Path

def main():
    config_path = Path("configs/experimento-base.yaml")
    
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    repr = cfg["reprodutibilidade"]
    repeticoes = repr["repeticoes_por_cenario"]

    print("=" * 60)
    print("Inicialização do programa")
    print("=" * 60)
    messages = [
        {"role": "system", "content": "Voce responde em pt-BR, em ate 3 linhas"},
        {"role": "user", "content": "O que e RAG? Responda de forma direta."},
    ]

    for i in range(repeticoes):
        t0, t1, resp = chamar_modelo(messages)
        n_in, n_out, custo = custo_chamada(messages, resp)
        registrar_log(resp, n_in, custo, t0, t1)
        print(f"{i + 1}ª iteracao de teste    [OK]")

    print("=" * 60)
    print("Finalização do programa")
    print("=" * 60)


if __name__ == "__main__":
    main()
