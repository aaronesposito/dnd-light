from db_connection import execute_query, execute_many
from queries.characters import get_one_character


def new_spell(data):
    query = """
        INSERT INTO spell (
            name,
            class,
            range,
            damage_die,
            num_of_dice,
            damage_type,
            area_type,
            cooldown,
            description
        ) VALUES (
            %(name)s,
            %(class)s,
            %(range)s,
            %(damage_die)s,
            %(num_of_dice)s,
            %(damage_type)s,
            %(area_type)s,
            %(cooldown)s,
            %(description)s
        )
        RETURNING id
    """
    result = execute_query(query, data, fetch_one=True)
    return result[0] if result else None

def get_spell(spell_id):
    query = """
            SELECT * FROM spell WHERE id = %s
        """
    data = execute_query(query, [spell_id], fetch_one=True)
    if data:
        return {
            "id":data[0],
            "name":data[1],
            "class":data[2],
            "range":data[3],
            "damage_die":data[4],
            "num_of_dice":data[5],
            "damage_type":data[6],
            "area_type":data[7],
            "cooldown":data[8],
            "description":data[9]
        }
    else:
        return None

def get_spells_by_class(class_id):
    query = """
            SELECT * FROM SPELL WHERE class = %s    
        """
    data = execute_many(query,[class_id])
    spells = []
    for row in data:
        spells.append({
            "id":row[0],
            "name":row[1],
            "class":row[2],
            "range":row[3],
            "damage_die":row[4],
            "num_of_dice":row[5],
            "damage_type":row[6],
            "area_type":row[7],
            "cooldown":row[8],
            "description":row[9]
        })
    return spells

def add_to_spellbook(data):
    character = get_one_character(data["character_id"])
    spell = get_spell(data["spell_id"])
    if character["class"]["id"] == spell["class"]:
        query = """
                INSERT INTO spellbook (
                    character_id,
                    spell_id
                )VALUES(
                    %(character_id)s,
                    %(spell_id)s
                );
            """
        data = execute_query(query, data, fetch_one=True)
        if data:
            return {
                "character_id":data[0],
                "spell_id":data[1]
            }
        else:
            return None
    else:
        raise ValueError("character class not eligible for spell")