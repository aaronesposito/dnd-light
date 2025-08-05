import psycopg2
from contextlib import contextmanager
from typing import Optional, Any, List, Tuple
from queries.DB_info import DB_DATA


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Automatically handles connection and cursor creation/closing.
    
    Usage:
        with get_db_connection() as (conn, cur):
            cur.execute("SELECT * FROM table")
            result = cur.fetchall()
    """
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_DATA)
        cur = conn.cursor()
        yield conn, cur
        conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def execute_query(query: str, params: Optional[Any] = None, fetch_one: bool = False, fetch_all: bool = False) -> Optional[Any]:
    """
    Execute a database query with automatic connection management.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch_one: If True, returns single row
        fetch_all: If True, returns all rows
        
    Returns:
        Query results if fetch_one or fetch_all is True, None otherwise
    """
    with get_db_connection() as (conn, cur):
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        
        if fetch_one:
            return cur.fetchone()
        elif fetch_all:
            return cur.fetchall()
        return None


def execute_many(query: str, params_list: List[Tuple]) -> None:
    """
    Execute multiple queries with the same statement but different parameters.
    
    Args:
        query: SQL query string
        params_list: List of parameter tuples
    """
    with get_db_connection() as (conn, cur):
        cur.executemany(query, params_list)
