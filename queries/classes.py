import psycopg2
from queries.DB_info import DB_DATA

def new_class(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO class (
                    name,
                    strength_bonus,
                    agility_bonus,
                    intellect_bonus
                ) VALUES 
                (%(name)s,
                %(strength_bonus)s,
                %(agility_bonus)s,
                %(intellect_bonus)s)
                """, data)
    cur.close()
    conn.commit()
    conn.close()

def update_class(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("""
                UPDATE class
                SET 
                    name = %(name)s,
                    strength_bonus = %(strength_bonus)s,
                    agility_bonus = %(agility_bonus)s,
                    intellect_bonus = %(intellect_bonus)s
                WHERE id = %(id)s""", data)
    cur.close()
    conn.commit()
    conn.close()

def get_all_classes():
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("SELECT * FROM class")
    data = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return data

def one_class(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("SELECT * FROM class where id = %s", [data])
    data = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()
    return {
            "id": data[0],
            "name": data[1],
            "strength_bonus": data[2],
            "agility_bonus": data[3],
            "intellect_bonus": data[4]
        }

def delete_class(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("DELETE FROM class WHERE id = %s", [data])
    cur.close()
    conn.commit()
    conn.close()
