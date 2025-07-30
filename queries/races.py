import psycopg2
from queries.DB_info import DB_DATA

def new_race(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO race (
                    name,
                    strength_bonus,
                    agility_bonus,
                    intellect_bonus,
                    racial_ability_name,
                    racial_ability_text
                ) VALUES 
                (%(name)s,
                %(strength_bonus)s,
                %(agility_bonus)s,
                %(intellect_bonus)s,
                %(racial_ability_name)s,
                %(racial_ability_text)s)
                """, data)
    cur.close()
    conn.commit()
    conn.close()

def update_race(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("""
                UPDATE race
                SET 
                    name = %(name)s,
                    strength_bonus = %(strength_bonus)s,
                    agility_bonus = %(agility_bonus)s,
                    intellect_bonus = %(intellect_bonus)s,
                    racial_ability_name = %(racial_ability_name)s,
                    racial_ability_text = %(racial_ability_text)s
                WHERE id = %(id)s""", data)
    cur.close()
    conn.commit()
    conn.close()

def get_all_races():
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("SELECT * FROM race")
    data = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return data

def one_race(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("SELECT * FROM race where id = %s", [data])
    data = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()
    return {
            "id": data[0],
            "name": data[1],
            "strength_bonus": data[2],
            "agility_bonus": data[3],
            "intellect_bonus": data[4],
            "racial_ability_name": data[5],
            "racial_ability_text": data[6]
        }

def delete_race(data):
    conn = psycopg2.connect(**DB_DATA)
    cur = conn.cursor()
    cur.execute("DELETE FROM race WHERE id = %s", [data])
    cur.close()
    conn.commit()
    conn.close()



