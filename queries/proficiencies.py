import psycopg2
from queries.DB_info import DB_DATA


def new_proficiency(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO %(proficiency)s_proficiency (
                    class_id,
                    %(proficiency)s_type
                ) VALUES 
                (%(class_id)s,
                %(type)s)
                """, data)
    cur.close()
    conn.commit()
    conn.close()

def get_all_proficiencies(type):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("SELECT * FROM class")
    data = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return data