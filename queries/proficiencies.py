from db_connection import execute_query


def prof_validation(prof_type):
    """
    Validate proficiency type and return table and column names.
    Raises ValueError if the type is invalid.
    """
    valid_types = {
        "weapon": ("weapon_proficiency", "weapon_type"),
        "armor": ("armor_proficiency", "armor_type"),
    }
    if prof_type not in valid_types:
        raise ValueError(f"Invalid proficiency type: must be one of {list(valid_types.keys())}")
    
    table, col = valid_types[prof_type]
    return table, col


def new_proficiency(data):
    """
    Insert a new proficiency into the database.
    Returns the ID of the created proficiency.
    """
    if "proficiency" not in data:
        raise ValueError("Missing required field: proficiency")
    if "class_id" not in data:
        raise ValueError("Missing required field: class_id")
    if "type" not in data:
        raise ValueError("Missing required field: type")
    
    table, col = prof_validation(data["proficiency"])
    
    # Use parameterized query for values only, table/column names are validated
    query = f"""
        INSERT INTO {table} (
            class_id,
            {col}
        ) VALUES (
            %(class_id)s,
            %(type)s
        )
        RETURNING id
    """
    result = execute_query(query, data, fetch_one=True)
    return result[0] if result else None


def get_all_proficiencies():
    """
    Retrieve all proficiencies from all proficiency tables.
    Returns a dictionary organized by proficiency type.
    """
    proficiencies = {}
    
    # Get weapon proficiencies
    weapon_query = """
        SELECT wp.id, wp.class_id, c.name as class_name, wp.weapon_type
        FROM weapon_proficiency wp
        JOIN class c ON c.id = wp.class_id
        ORDER BY wp.id
    """
    weapon_data = execute_query(weapon_query, fetch_all=True)
    proficiencies["weapon"] = []
    for row in weapon_data:
        proficiencies["weapon"].append({
            "id": row[0],
            "class_id": row[1],
            "class_name": row[2],
            "type": row[3]
        })
    
    # Get armor proficiencies
    armor_query = """
        SELECT ap.id, ap.class_id, c.name as class_name, ap.armor_type
        FROM armor_proficiency ap
        JOIN class c ON c.id = ap.class_id
        ORDER BY ap.id
    """
    armor_data = execute_query(armor_query, fetch_all=True)
    proficiencies["armor"] = []
    for row in armor_data:
        proficiencies["armor"].append({
            "id": row[0],
            "class_id": row[1],
            "class_name": row[2],
            "type": row[3]
        })
    
    return proficiencies


def get_proficiencies_by_type(prof_type):
    """
    Retrieve all proficiencies of a specific type, grouped by class.
    Returns a dictionary with class names as keys and lists of proficiency types as values.
    """
    table, col = prof_validation(prof_type)
    
    query = f"""
        SELECT c.id, c.name, p.{col}
        FROM class c
        JOIN {table} p ON c.id = p.class_id
        ORDER BY c.name, p.{col}
    """
    data_list = execute_query(query, fetch_all=True)
    
    # Group by class
    result = []
    class_dict = {}
    
    for row in data_list:
        class_id, class_name, prof_value = row
        if class_id not in class_dict:
            class_dict[class_id] = {
                "class_id": class_id,
                "class_name": class_name,
                "proficiencies": []
            }
        class_dict[class_id]["proficiencies"].append(prof_value)
    
    # Convert to list
    result = list(class_dict.values())
    return result


def get_proficiencies_for_class(class_id, proficiency_type):
    """
    Get all proficiencies of a specific type for a given class.
    Returns an object with class information and proficiencies.
    """
    table, col = prof_validation(proficiency_type)
    
    query = f"""
        SELECT c.id, c.name, p.{col}
        FROM class c
        LEFT JOIN {table} p ON c.id = p.class_id
        WHERE c.id = %s
        ORDER BY p.{col}
    """
    data_list = execute_query(query, [class_id], fetch_all=True)
    
    if not data_list:
        return None
    
    # Build result
    result = {
        "class_id": data_list[0][0],
        "class_name": data_list[0][1],
        "proficiency_type": proficiency_type,
        "proficiencies": []
    }
    
    for row in data_list:
        if row[2] is not None:  # Skip NULL proficiencies
            result["proficiencies"].append(row[2])
    
    return result
