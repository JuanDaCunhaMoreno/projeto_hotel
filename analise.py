import pandas as pd
import sqlite3

try:
    df_hotel = pd.read_excel('HotelCustomersDataset.xlsx')
    print("-> Arquivo carregado com sucesso!")
except FileNotFoundError:
    print("Erro: Arquivo não foi carregado!")
    exit()

#Corrigir age float/null...
media_age = df_hotel['Age'].mean()
df_hotel['Age'] = df_hotel['Age'].fillna(media_age).astype(int)

df_hotel = df_hotel.rename(columns = {
    'DaysSinceLastStay': 'Recency',
    'RoomNights': 'Frequency',
    'LodgingRevenue': 'Monetary'
})

df_hotel['R_Score'] = pd.qcut(df_hotel['Recency'], 4, labels = [4, 3, 2, 1])
df_hotel['F_Score'] = pd.qcut(df_hotel['Frequency'].rank(method = 'first'), 4, labels = [1, 2, 3, 4])
df_hotel['M_Score'] = pd.qcut(df_hotel['Monetary'].rank(method = 'first'), 4, labels = [1, 2, 3, 4])
df_hotel['RFM_Score'] = df_hotel['R_Score'].astype(str) + df_hotel['F_Score'].astype(str) + df_hotel['M_Score'].astype(str)

segment_map = {
    r'[3-4][3-4][3-4]': 'Campeões',
    r'[2-4][1-3][1-3]': 'Clientes Fiéis',
    r'[3-4][1-2][1-4]': 'Potencialmente Fiéis',
    r'[3-4]44': 'Novos Clientes',
    r'1[1-4][1-4]': 'Em Risco',
    r'2[3-4][3-4]': 'Precisam de Atenção',
    r'[1-2][1-2][1-2]': 'Hibernando'
}

df_hotel['Segmento'] = df_hotel['RFM_Score'].replace(segment_map, regex=True)
df_hotel['Segmento'] = df_hotel['Segmento'].replace(to_replace=r'^\d+$', value='Outros', regex=True)

print(df_hotel['Segmento'].value_counts())

#SQL
db_name = 'hotel.db'
conn = sqlite3.connect(db_name)
print(f"-> Conexão criada com o banco de dados '{db_name}' estabelecida com sucesso!")

df_hotel.to_sql('clientes', conn, if_exists = 'replace', index = False)
print("-> DataFrame salvo na tabela 'clientes' com sucesso.")
conn.close()
