import psycopg2

# Defina as informações de conexão
host = "localhost"
database = "pool"
user = "postgres"
password = "123456789"

# Faça a conexão
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

# Execute uma consulta
cur = conn.cursor()
cur.execute("SELECT * FROM alunos;")
rows = cur.fetchall()
print(rows)

# Feche a conexão
cur.close()
conn.close()
