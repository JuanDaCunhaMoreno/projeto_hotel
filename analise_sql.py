import pandas as pd
import sqlite3

db_name = 'hotel.db'
conn = sqlite3.connect(db_name)
print(f"-> Conectado ao banco de dados: {db_name}")

print("Contagem Clientes por Segmento: ")
query_segmentos = """
SELECT
    Segmento,
    COUNT(ID) as TotalClientes
FROM
    clientes
GROUP BY
    Segmento
ORDER BY
    TotalClientes DESC;
"""

df_segmentos = pd.read_sql_query(query_segmentos, conn)
print(df_segmentos)
