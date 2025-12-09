from abc import ABC, abstractmethod
from flask import current_app
import psycopg2 
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import json
from urllib.parse import urlparse
from config import config
import os
from flask_sqlalchemy import SQLAlchemy

db : object = SQLAlchemy()

class db_gestion(ABC):

    @abstractmethod
    def init_conexion(self):
        pass

    @abstractmethod 
    def release_conexion(self, *args, **kwargs):
        pass


class Db_gestion_postgres(db_gestion):

    def init_conexion(self):
        if not hasattr(current_app, 'db_pool'):
            db_uri = config.SQLALCHEMY_DATABASE_URI
            parsed = urlparse(db_uri)
            
            minconn = 5 
            maxconn = 50  

            current_app.db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn, maxconn,
                host=parsed.hostname,
                port=parsed.port or 5432,
                database=parsed.path.lstrip('/'),
                user=parsed.username,
                password=parsed.password
            )

        return current_app.db_pool.getconn()
        
    def release_conexion(self, conn):
        if hasattr(current_app, 'db_pool'):
            return current_app.db_pool.putconn(conn)


"""
    SQL Query Executor - Loads and executes SQL queries from .sql files

    This class provides a clean interface to execute database operations by loading
    SQL queries from external .sql files in the 'querys' folder.

    Attributes:
        db_manager (Db_gestion_postgres): Database connection manager instance
        queries_path (str): Path to the folder containing .sql files

    Usage Examples:

        # 1. Initialize the query executor
        db_manager = Db_gestion_postgres()
        query_exec = Query_execute(db_manager)
        
        # 2. SELECT ALL - Get all users
        # File: querys/get_all_users.sql
        # SQL: SELECT * FROM users ORDER BY created_at DESC;
        users = query_exec.execute_query_from_file('get_all_users.sql')
        # Returns: [{'id': 1, 'name': 'John', 'email': 'john@email.com'}, ...]
        
        # 3. SELECT ONE - Get user by email
        # File: querys/get_user_by_email.sql
        # SQL: SELECT * FROM users WHERE email = %s;
        user = query_exec.execute_query_from_file(
            'get_user_by_email.sql',
            params=('john@email.com',),
            fetch_one=True
        )
        # Returns: {'id': 1, 'name': 'John', 'email': 'john@email.com'} or None
        
        # 4. SELECT with multiple parameters
        # File: querys/search_products.sql
        # SQL: SELECT * FROM products WHERE category = %s AND price BETWEEN %s AND %s;
        products = query_exec.execute_query_from_file(
            'search_products.sql',
            params=('electronics', 100, 500)
        )
        # Returns: [{'id': 1, 'name': 'Phone', 'price': 299}, ...]
        
        # 5. INSERT - Create new user
        # File: querys/create_user.sql
        # SQL: INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;
        result = query_exec.execute_insert_from_file(
            'create_user.sql',
            params=('John Doe', 'john@email.com', 'hashed_password'),
            return_id=True
        )
        # Returns: {'success': True, 'code': 0, 'message': '...', 'id': 42}
        
        # 6. UPDATE - Update user data
        # File: querys/update_user.sql
        # SQL: UPDATE users SET name = %s, email = %s WHERE id = %s;
        result = query_exec.execute_insert_from_file(
            'update_user.sql',
            params=('Jane Doe', 'jane@email.com', 1)
        )
        # Returns: {'success': True, 'code': 0, 'message': '...'}
        
        # 7. DELETE - Delete user
        # File: querys/delete_user.sql
        # SQL: DELETE FROM users WHERE id = %s;
        result = query_exec.execute_insert_from_file(
            'delete_user.sql',
            params=(1,)
        )
        # Returns: {'success': True, 'code': 0, 'message': '...'} or error dict

    Methods:
        __init__(db_manager): Initialize with a database manager
        _load_sql_file(filename): Load SQL content from a file (private method)
        execute_query_from_file(sql_filename, params, fetch_one): Execute SELECT queries
        execute_insert_from_file(sql_filename, params, return_id): Execute INSERT/UPDATE/DELETE
"""
class Query_execute():
    def __init__(self, db_manager: Db_gestion_postgres):
        self.db_manager = db_manager
        self.queries_path = os.path.join(os.path.dirname(__file__), 'querys')


    def _load_sql_file(self, filename):
        file_path = os.path.join(self.queries_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"SQL file not found: {filename}")
        except Exception as e:
            raise Exception(f"Error reading SQL file {filename}: {str(e)}")


    def execute_query_from_file(self, sql_filename, params=None, fetch_one=False):
        query = self._load_sql_file(sql_filename)
        conn = self.db_manager.init_conexion()
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            else:
                results = cursor.fetchall()
                return [dict(row) for row in results]
                
        except Exception as e:
            error_response = {
                "success": False,
                "code": getattr(e, 'pgcode', 'UNKNOWN'),
                "message": f"Error executing query from {sql_filename}: {str(e)}"
            }
            print(f"Error: {error_response}")
            raise Exception(json.dumps(error_response))
        finally:
            cursor.close()
            self.db_manager.release_conexion(conn)


    def execute_insert_from_file(self, sql_filename, params=None, return_id=False):
        query = self._load_sql_file(sql_filename)
        conn = self.db_manager.init_conexion()
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            conn.commit()
            
            inserted_id = None
            if return_id:
                result = cursor.fetchone()
                if result and 'id' in result:
                    inserted_id = result['id']
            
            response = {
                "success": True,
                "code": 0,
                "message": f"Operation executed successfully from {sql_filename}"
            }
            
            if inserted_id is not None:
                response["id"] = inserted_id
                
            return response
            
        except Exception as e:
            conn.rollback()
            error_response = {
                "success": False,
                "code": getattr(e, 'pgcode', 'UNKNOWN'),
                "message": f"Error executing insert from {sql_filename}: {str(e)}"
            }
            print(f"Error: {error_response}")
            return error_response
        finally:
            cursor.close()
            self.db_manager.release_conexion(conn)


db_manager = Db_gestion_postgres()
query_exec = Query_execute(db_manager)