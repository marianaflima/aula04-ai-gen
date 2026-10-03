import importlib
import platform
import sys

obrigatorios = ["openai", "tiktoken", "dotenv","rich", "sklearn", "pyyaml", "groq"]

print(f"Python {sys.version.split()[0]}"
      f"({platform.machine()})")

for module in obrigatorios:
    importlib.import_module(module)
    print(f"      [OK] {module}")

print("Ambiente pronto para o LabIA.")