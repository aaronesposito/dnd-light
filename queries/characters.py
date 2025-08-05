from db_connection import execute_query, execute_many
from queries.classes import get_class
from queries.races import get_race


def create_character(data):

    race_data = get_race(data["race"])
    class_data = get_class(data["class"])
    stats = ["strength", "agility", "intellect"]
    for key in stats:
        data[key] += race_data[key+"_bonus"] + class_data[key+"_bonus"]
    
    query = """
            INSERT INTO character (
                name,
                race,
                class,
                strength,
                agility,
                intellect
            ) VALUES (
                %(name)s,
                %(race)s,
                %(class)s,
                %(strength)s,
                %(agility)s,
                %(intellect)s
            )
            """
    execute_query(query, data)

def get_all_characters():
    query = """
                SELECT  char.id,
                        char.name, 
                        race.name, 
                        class.name, 
                        char.level, 
                        char.hp, 
                        char.mana, 
                        char.strength, 
                        char.agility, 
                        char.intellect, 
                        char.defense, 
                        char.armor_id, 
                        char.weapon_id, 
                        char.gold 
                FROM character as char
                JOIN race on race.id = char.race
                JOIN class on class.id = char.class
                """
    data = execute_query(query, fetch_all=True)
    characters = []
    for row in data:
        characters.append(
        {row[1]:{
            "id": row[0],
            "race": row[2],
            "class": row[3],
            "level": row[4],
            "hp": row[5],
            "mana": row[6],
            "strength": row[7],
            "agility": row[8],
            "intellect": row[9],
            "defense": row[10],
            "armor_id": row[11],
            "weapon_id": row[12],
            "gold":row[13]
        }})
    return characters

def get_one_character(data):
    query= """
            SELECT  char.id,
                    char.name, 
                    race.name, 
                    class.name, 
                    char.level, 
                    char.hp, 
                    char.mana, 
                    char.strength, 
                    char.agility, 
                    char.intellect, 
                    char.defense, 
                    char.armor_id, 
                    char.weapon_id, 
                    char.gold 
            FROM character as char
            JOIN race on race.id = char.race
            JOIN class on class.id = char.class
            WHERE char.id = %s
            """
    character = execute_query(query, [data], fetch_one=True)
    return   {character[1]:{
            "id": character[0],
            "race": character[2],
            "class": character[3],
            "level": character[4],
            "hp": character[5],
            "mana": character[6],
            "strength": character[7],
            "agility": character[8],
            "intellect": character[9],
            "defense": character[10],
            "armor_id": character[11],
            "weapon_id": character[12],
            "gold":character[13]
        }}

def delete_character(data):
    query = "DELETE FROM character WHERE id = %s"
    execute_query(query, [data])
