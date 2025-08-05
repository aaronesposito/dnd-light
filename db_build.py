import psycopg2
from dotenv import load_dotenv
from db_connection import get_db_connection


load_dotenv()

TYPE_BUILD = {
    "item_type": """CREATE TYPE item_type AS ENUM (
        'weapon',
        'armor',
        'consumable',
        'quest',
        'misc'
    )""",

    "armor_type": """CREATE TYPE armor_type AS ENUM (
        'light',
        'medium',
        'heavy',
        'magical'
    )""",

    "weapon_type": """CREATE TYPE weapon_type AS ENUM (
        'sword',
        'axe',
        'bow',
        'staff',
        'wand'
    )""",

    "consumable_type": """CREATE TYPE consumable_type AS ENUM (
        'potion',
        'food'
    );""",
}

TABLE_BUILD = [
    """CREATE TABLE IF NOT EXISTS race (
        id SERIAL PRIMARY KEY,
        name VARCHAR(25) NOT NULL UNIQUE,
        strength_bonus INT DEFAULT 0,
        agility_bonus INT DEFAULT 0,
        intellect_bonus INT DEFAULT 0,
        racial_ability_name VARCHAR(50),
        racial_ability_text TEXT
    );""",

    """CREATE TABLE IF NOT EXISTS class (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        strength_bonus INT DEFAULT 0,
        agility_bonus INT DEFAULT 0,
        intellect_bonus INT DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS armor_proficiency (
        class_id INT REFERENCES class(id) ON DELETE CASCADE,
        armor_type armor_type NOT NULL,
        PRIMARY KEY (class_id, armor_type)
    );""",

    """CREATE TABLE IF NOT EXISTS weapon_proficiency (
        class_id INT REFERENCES class(id) ON DELETE CASCADE,
        weapon_type weapon_type NOT NULL,
        PRIMARY KEY (class_id, weapon_type)
    );""",

    """CREATE TABLE IF NOT EXISTS item (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        value INT DEFAULT 0,
        weight int DEFAULT 0,
        description TEXT,
    
        weapon_type weapon_type,
        damage int DEFAULT 0,
        magic_damage int DEFAULT 0,
        weapon_required_strength INT DEFAULT 0,
        weapon_required_agility INT DEFAULT 0,
        weapon_required_intellect INT DEFAULT 0,
    
        armor_type armor_type,
        defense int DEFAULT 0,
        magic_resist int DEFAULT 0,
        armor_required_strength int DEFAULT 0,
    
        consumable_type consumable_type,
        health_restore int DEFAULT 0,
        mana_restore int DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS character (
        id SERIAL PRIMARY KEY,
        is_active BOOL DEFAULT FALSE,
        name VARCHAR(100) NOT NULL UNIQUE,
        race INT REFERENCES race(id),
        class INT REFERENCES class(id),
        level INT DEFAULT 1,
        hp INT NOT NULL DEFAULT 100,
        mana INT DEFAULT 50,
        strength INT DEFAULT 10,
        agility INT DEFAULT 10,
        intellect INT DEFAULT 10,
        defense INT DEFAULT 10,
        armor_id INT REFERENCES item(id),
        weapon_id INT REFERENCES item(id),
        gold INT NOT NULL DEFAULT 0
    );""",

    """CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        character INT REFERENCES character(id),
        item INT REFERENCES item(id),
        slot_number INT CHECK (slot_number BETWEEN 1 AND 10)
    );"""
]


def DB_init():
    """Initialize the database with types and tables."""
    with get_db_connection() as (conn, cur):
        # Create custom types
        for type_name, command in TYPE_BUILD.items():
            try:
                cur.execute(f"SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{type_name}');")
                exists = cur.fetchone()[0]
                if not exists:
                    cur.execute(command)
                    print(f"Created type: {type_name}")
            except psycopg2.Error as e:
                print(f"Error creating type {type_name}: {e}")
                # Continue with other types even if one fails
                conn.rollback()
        
        # Create tables
        for command in TABLE_BUILD:
            try:
                cur.execute(command)
                # Extract table name for logging
                table_name = command.split("CREATE TABLE IF NOT EXISTS ")[1].split()[0]
                print(f"Created/verified table: {table_name}")
            except psycopg2.Error as e:
                print(f"Error creating table: {e}")
                conn.rollback()
