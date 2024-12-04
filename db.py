import psycopg2
from psycopg2.extras import RealDictCursor

db_config = {
    "dbname": "myowndb",
    "user": "burnedrice",
    "password": "postgres123",
    "host": "localhost",
    "port": 5432
}

def conectar_banco():
    try:
        return psycopg2.connect(**db_config)
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def executar_query(query, parametros=None):
    conn = conectar_banco()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, parametros)
                if query.strip().lower().startswith("select"):
                    return cur.fetchall()
                if "returning" in query.strip().lower():
                    resultado = cur.fetchone()
                    conn.commit() 
                    return resultado
                conn.commit()
                return None
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            raise
        finally:
            conn.close()
