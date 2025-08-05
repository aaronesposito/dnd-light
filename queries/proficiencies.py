from db_connection import execute_query


def prof_validation(type):
    valid_types = {
        "weapon": ("weapon_proficiency", "weapon_type"),
        "armor": ("armor_proficiency", "armor_type"),
    }
    if type not in valid_types:
        raise ValueError(f"invalid proficiency type: must be one of [weapon, armor]")
    
    table, col = valid_types[type]
    return table, col


def new_proficiency(data):
    """Insert a new proficiency into the database."""
    # Note: This query uses string formatting for table name which could be a security risk
    # In production, you should validate the proficiency type against a whitelist
    
    table, col = prof_validation(data["proficiency"])
    query = f"""
        INSERT INTO {table} (
            class_id,
            {col}
        ) VALUES 
        (%(class_id)s,
        %(type)s)
    """
    execute_query(query, data)


def get_all_proficiencies(type):
    """
    Retrieve all proficiencies of a specific type.
    """
    table, col = prof_validation(type)
    query = f"SELECT * FROM {table}"
    return execute_query(query, type, fetch_all=True)


def get_proficiencies_by_type(type):
    """
    Retrieve all proficiencies of a specific type.
    This is a corrected version that actually queries the proficiency table.
    """
    # Validate proficiency_type to prevent SQL injection
    table, col = prof_validation(type)
    
    # Using string formatting for table name - be careful with this
    query = f"SELECT class.name, prof.{col}  FROM class JOIN {table} as prof on class.id = prof.class_id"
    data_list = execute_query(query, fetch_all=True)
    data = {}
    for row in data_list:
        if row[0] in data:
            data[row[0]].append(row[1])
        else:
            data[row[0]] = [row[1]]
    return data


def get_proficiencies_for_class(class_id, proficiency_type):
    """Get all proficiencies of a specific type for a given class."""
    table, col = prof_validation(proficiency_type)
    query = f"SELECT class.name, {table}.{col} FROM {table} LEFT JOIN class on class.id = {table}.class_id WHERE {table}.class_id = {class_id}"
    data_list = execute_query(query, [class_id], fetch_all=True)
    return {data_list[0][0]:[item[1] for item in data_list]}
