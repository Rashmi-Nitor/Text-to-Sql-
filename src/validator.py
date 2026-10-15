import sqlglot
ALLOWED = ["SELECT"]
 
 
def validate(sql):
 
    sql = sql.strip()
 
    if not sql.upper().startswith("SELECT"):
        return False, "Only SELECT queries allowed"
 
    try:
        sqlglot.parse_one(sql)
    except Exception as e:
        return False, str(e)
 
    return True, "Valid SQL"