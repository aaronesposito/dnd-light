from db_connection import execute_query, get_db_connection


def new_class(data):
    """
    Insert a new class into the database.
    Returns the ID of the created class.
    """
    query = """
        INSERT INTO class (
            name,
            strength_bonus,
            agility_bonus,
            intellect_bonus
        ) VALUES (
            %(name)s,
            %(strength_bonus)s,
            %(agility_bonus)s,
            %(intellect_bonus)s
        )
        RETURNING id
    """
    result = execute_query(query, data, fetch_one=True)
    return result[0] if result else None


def update_class(class_id, data):
    """Update an existing class in the database."""
    # Build dynamic update query based on provided fields
    update_fields = []
    params = {"id": class_id}
    
    allowed_fields = ["name", "strength_bonus", "agility_bonus", "intellect_bonus"]
    
    for field in allowed_fields:
        if field in data:
            update_fields.append(f"{field} = %({field})s")
            params[field] = data[field]
    
    if not update_fields:
        raise ValueError("No valid fields to update")
    
    query = f"""
        UPDATE class
        SET {', '.join(update_fields)}
        WHERE id = %(id)s
    """
    execute_query(query, params)


def get_all_classes():
    """
    Retrieve all classes from the database.
    Returns a list of class objects with consistent structure.
    """
    query = """
        SELECT id, name, strength_bonus, agility_bonus, intellect_bonus
        FROM class
        ORDER BY id
    """
    data = execute_query(query, fetch_all=True)
    classes = []
    for row in data:
        classes.append({
            "id": row[0],
            "name": row[1],
            "strength_bonus": row[2],
            "agility_bonus": row[3],
            "intellect_bonus": row[4]
        })
    return classes


def get_class(class_id):
    """
    Retrieve a single class by ID.
    Returns a class object or None if not found.
    """
    query = """
        SELECT id, name, strength_bonus, agility_bonus, intellect_bonus
        FROM class 
        WHERE id = %s
    """
    data = execute_query(query, [class_id], fetch_one=True)
    
    if data:
        return {
            "id": data[0],
            "name": data[1],
            "strength_bonus": data[2],
            "agility_bonus": data[3],
            "intellect_bonus": data[4]
        }
    return None


def delete_class(class_id):
    """Delete a class from the database."""
    query = "DELETE FROM class WHERE id = %s"
    execute_query(query, [class_id])
