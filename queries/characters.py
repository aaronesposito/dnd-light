from db_connection import execute_query, execute_many
from queries.classes import get_class
from queries.races import get_race


def create_character(data):
    """
    Create a new character with calculated stats.
    Returns the ID of the created character.
    """
    race_data = get_race(data["race"])
    class_data = get_class(data["class"])
    
    if not race_data or not class_data:
        raise ValueError("Invalid race or class ID")
    
    stats = ["strength", "agility", "intellect"]
    for key in stats:
        data[key] = data.get(key, 0) + race_data[key+"_bonus"] + class_data[key+"_bonus"]
    
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
            RETURNING id
            """
    result = execute_query(query, data, fetch_one=True)
    return result[0] if result else None


def get_all_characters():
    """
    Retrieve all characters from the database.
    Returns a list of character objects with consistent structure.
    """
    query = """
                SELECT  char.id,
                        char.name, 
                        race.name as race_name, 
                        class.name as class_name, 
                        char.level, 
                        char.hp, 
                        char.mana, 
                        char.strength, 
                        char.agility, 
                        char.intellect, 
                        char.defense, 
                        char.armor_id, 
                        char.weapon_id, 
                        char.gold,
                        char.race as race_id,
                        char.class as class_id
                FROM character as char
                JOIN race on race.id = char.race
                JOIN class on class.id = char.class
                ORDER BY char.id
                """
    data = execute_query(query, fetch_all=True)
    characters = []
    for row in data:
        characters.append({
            "id": row[0],
            "name": row[1],
            "race": {
                "id": row[14],
                "name": row[2]
            },
            "class": {
                "id": row[15],
                "name": row[3]
            },
            "level": row[4],
            "hp": row[5],
            "mana": row[6],
            "strength": row[7],
            "agility": row[8],
            "intellect": row[9],
            "defense": row[10],
            "armor_id": row[11],
            "weapon_id": row[12],
            "gold": row[13]
        })
    return characters


def get_one_character(character_id):
    """
    Retrieve a single character by ID.
    Returns a character object or None if not found.
    """
    query = """
            SELECT  char.id,
                    char.name, 
                    race.name as race_name, 
                    class.name as class_name, 
                    char.level, 
                    char.hp, 
                    char.mana, 
                    char.strength, 
                    char.agility, 
                    char.intellect, 
                    char.defense, 
                    char.armor_id, 
                    char.weapon_id, 
                    char.gold,
                    char.race as race_id,
                    char.class as class_id
            FROM character as char
            JOIN race on race.id = char.race
            JOIN class on class.id = char.class
            WHERE char.id = %s
            """
    character = execute_query(query, [character_id], fetch_one=True)
    
    if character:
        return {
            "id": character[0],
            "name": character[1],
            "race": {
                "id": character[14],
                "name": character[2]
            },
            "class": {
                "id": character[15],
                "name": character[3]
            },
            "level": character[4],
            "hp": character[5],
            "mana": character[6],
            "strength": character[7],
            "agility": character[8],
            "intellect": character[9],
            "defense": character[10],
            "armor_id": character[11],
            "weapon_id": character[12],
            "gold": character[13]
        }
    return None


def update_character(character_id, data):
    """Update an existing character in the database."""
    # Build dynamic update query based on provided fields
    update_fields = []
    params = {"id": character_id}
    
    allowed_fields = ["name", "race", "class", "level", "hp", "mana", 
                      "strength", "agility", "intellect", "defense", 
                      "armor_id", "weapon_id", "gold"]
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f"{field} = %({field})s")
            params[field] = data[field]
    
    if not update_fields:
        raise ValueError("No valid fields to update")
    
    query = f"""
        UPDATE character
        SET {', '.join(update_fields)}
        WHERE id = %(id)s
    """
    execute_query(query, params)


def delete_character(character_id):
    """Delete a character from the database."""
    query = "DELETE FROM character WHERE id = %s"
    execute_query(query, [character_id])
