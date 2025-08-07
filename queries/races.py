from db_connection import execute_query


def new_race(data):
    """
    Insert a new race into the database.
    Returns the ID of the created race.
    """
    query = """
        INSERT INTO race (
            name,
            strength_bonus,
            agility_bonus,
            intellect_bonus,
            racial_ability_name,
            racial_ability_text
        ) VALUES (
            %(name)s,
            %(strength_bonus)s,
            %(agility_bonus)s,
            %(intellect_bonus)s,
            %(racial_ability_name)s,
            %(racial_ability_text)s
        )
        RETURNING id
    """
    result = execute_query(query, data, fetch_one=True)
    return result[0] if result else None


def update_race(race_id, data):
    """Update an existing race in the database."""
    # Build dynamic update query based on provided fields
    update_fields = []
    params = {"id": race_id}
    
    allowed_fields = ["name", "strength_bonus", "agility_bonus", 
                      "intellect_bonus", "racial_ability_name", "racial_ability_text"]
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f"{field} = %({field})s")
            params[field] = data[field]
    
    if not update_fields:
        raise ValueError("No valid fields to update")
    
    query = f"""
        UPDATE race
        SET {', '.join(update_fields)}
        WHERE id = %(id)s
    """
    execute_query(query, params)


def get_all_races():
    """
    Retrieve all races from the database.
    Returns a list of race objects with consistent structure.
    """
    query = """
        SELECT id, name, strength_bonus, agility_bonus, intellect_bonus, 
               racial_ability_name, racial_ability_text
        FROM race
        ORDER BY id
    """
    data = execute_query(query, fetch_all=True)
    races = []
    for row in data:
        races.append({
            "id": row[0],
            "name": row[1],
            "strength_bonus": row[2],
            "agility_bonus": row[3],
            "intellect_bonus": row[4],
            "racial_ability_name": row[5],
            "racial_ability_text": row[6]
        })
    return races


def get_race(race_id):
    """
    Retrieve a single race by ID.
    Returns a race object or None if not found.
    """
    query = """
        SELECT id, name, strength_bonus, agility_bonus, intellect_bonus,
               racial_ability_name, racial_ability_text
        FROM race 
        WHERE id = %s
    """
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
