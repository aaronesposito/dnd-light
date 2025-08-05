from db_connection import execute_query, get_db_connection


def new_class(data):
    """Insert a new class into the database."""
    query = """
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
    """
    execute_query(query, data)


def update_class(data):
    """Update an existing class in the database."""
    query = """
        UPDATE class
        SET 
            name = %(name)s,
            strength_bonus = %(strength_bonus)s,
            agility_bonus = %(agility_bonus)s,
            intellect_bonus = %(intellect_bonus)s
        WHERE id = %(id)s
    """
    execute_query(query, data)


def get_all_classes():
    """Retrieve all classes from the database."""
    query = "SELECT * FROM class"
    data = execute_query(query, fetch_all=True)
    return_data = []
    for row in data:
        return_data.append({
            "id": row[0],
            "name": row[1],
            "strength_bonus": row[2],
            "agility_bonus": row[3],
            "intellect_bonus": row[4]
        })
    return return_data


def get_class(class_id):
    """Retrieve a single class by ID."""
    query = "SELECT * FROM class WHERE id = %s"
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
