from db_connection import execute_query


def new_race(data):
    """Insert a new race into the database."""
    query = """
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
    """
    execute_query(query, data)


def update_race(data):
    """Update an existing race in the database."""
    query = """
        UPDATE race
        SET 
            name = %(name)s,
            strength_bonus = %(strength_bonus)s,
            agility_bonus = %(agility_bonus)s,
            intellect_bonus = %(intellect_bonus)s,
            racial_ability_name = %(racial_ability_name)s,
            racial_ability_text = %(racial_ability_text)s
        WHERE id = %(id)s
    """
    execute_query(query, data)


def get_all_races():
    """Retrieve all races from the database."""
    query = "SELECT * FROM race"
    data = execute_query(query, fetch_all=True)
    return_data = []
    for row in data:
        return_data.append(
                {
                "id":row[0],
                "name":row[1],
                "strength_bonus": row[2],
                "agility_bonus": row[3],
                "intellect_bonus": row[4],
                "racial_ability_name": row[5],
                "racial_ability_text": row[6]
            }
        )
    return return_data


def get_race(race_id):
    """Retrieve a single race by ID."""
    query = "SELECT * FROM race WHERE id = %s"
    data = execute_query(query, [race_id], fetch_one=True)
    
    if data:
        return {
            "id": data[0],
            "name": data[1],
            "strength_bonus": data[2],
            "agility_bonus": data[3],
            "intellect_bonus": data[4],
            "racial_ability_name": data[5],
            "racial_ability_text": data[6]
        }
    return None


def delete_race(race_id):
    """Delete a race from the database."""
    query = "DELETE FROM race WHERE id = %s"
    execute_query(query, [race_id])
