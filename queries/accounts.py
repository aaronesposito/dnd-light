from db_connection import execute_query
import uuid


def check_duplicate_username(username):
    query = """
            SELECT username from account where username = %s
            """
    
    result = execute_query(query, [username], fetch_one=True)
    print(result)
    return result

def create_user(data):
    data["public_id"] = str(uuid.uuid4())
    query = """
            INSERT INTO account (
                public_id,
                username,
                password
            ) VALUES (
                %(public_id)s,
                %(username)s,
                %(password)s
            )
            RETURNING id
            """
    result = execute_query(query, data, fetch_one=True)
    return result[0] if result else None

def validate_account(username):
    query = "SELECT username, password, public_id FROM account WHERE username=%s"
    result = execute_query(query, [username], fetch_one=True)
    return {"username":result[0], "password_hash": result[1]}