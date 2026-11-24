import requests
from qdrant_client import QdrantClient

GOLDEN = [
    ("Сколько дней отпуска в год?", "01_otpusk.md"),
    ("Какие суточные при поездке за границу?", "02_komandirovki.md"),
    ("Какой минимальный размер пароля?", "03_infobez.md"),
    ("Сколько предложений нужно для закупки на 600 тысяч?", "04_zakupki.md"),
    ("Сколько длится испытательный срок?", "05_onboarding.md"),
]
qd = QdrantClient(url="http://localhost:6333")
ok = 0
for q, doc in GOLDEN:
    v = requests.post("http://localhost:11434/api/embed", json={"model": "bge-m3", "input": [q]}).json()["embeddings"][0]
    found = [h.payload["doc"] for h in qd.query_points("regulations", query=v, limit=3).points]
    ok += doc in found
    print(("OK  " if doc in found else "MISS"), q, "->", found)
print(f"recall@3 = {ok}/{len(GOLDEN)}")
