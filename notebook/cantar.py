"""Lee en voz alta el texto de Payikos.txt con la voz de macOS (`say`).

No es la voz de Anuel: solo usa una voz de sistema en español.
Uso: python notebook/cantar.py [voz]   (por defecto "Jorge")
"""
import subprocess
import sys
from pathlib import Path

voz = sys.argv[1] if len(sys.argv) > 1 else "Jorge"
ruta = Path(__file__).with_name("Payikos.txt")

# Nos quedamos con las líneas que son sobre todo letras (se saltan los dibujos ASCII).
lineas = [
    l.strip()
    for l in ruta.read_text(encoding="utf-8").splitlines()
    if l.strip() and sum(c.isalpha() or c == " " for c in l) / len(l) > 0.8
]

subprocess.run(["say", "-v", voz, "-r", "170", ". ".join(lineas)], check=True)
