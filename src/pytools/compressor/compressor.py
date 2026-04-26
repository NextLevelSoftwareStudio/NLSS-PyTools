import lzma
def compress_text_max(text: str, encoding: str = "utf-8"):
    dados = text.encode(encoding)
    filtros_maximos = [
    {
        "id": lzma.FILTER_LZMA2,
        "dict_size": 1536 * 1024 * 1024, # 1.5 GB (Limite prático do LZMA2)
        "mf": lzma.MF_BT4,               # O buscador mais exaustivo (Binary Tree 4)
        "mode": lzma.MODE_NORMAL,        # Análise profunda de bytes
        "nice_len": 273,                 # O limite máximo de match do algoritmo
        "lc": 4,                         # Máximo de bits de contexto literal
        "lp": 0,                         # Literal pos bits
        "pb": 2,                         # Pos bits (ideal para texto/strings)
        "depth": 0,                      # 0 define busca automática infinita (sem limite de ciclos)
    }
    ]
    try:
        comprimido = lzma.compress(dados, format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256, filters=filtros_maximos)
    except MemoryError:
        print("Error: ≥1,5 GiB RAM needed.")
def compress_bytes_max(bytes):
    pass