if __package__:
    from .db import get_connection
else:
    from db import get_connection


def execute_query(sql):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()

def compare_results(
    gold_sql,
    generated_sql
):
 
    gold_result = execute_query(gold_sql)
 
    generated_result = execute_query(
        generated_sql
    )
 
    return gold_result == generated_result