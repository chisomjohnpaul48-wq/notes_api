## UserCreate
def create_user(conn, name: str, email: str, password_hash: str):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id;
""", (name, email, password_hash))
        user_id = cur.fetchone()[0]
        conn.commit()
    return user_id

## NoteCreate
def create_note(conn, user_id, title, content):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO notes (user_id, title, content)
            VALUES (%s, %s, %s);
            """, (user_id, title, content))
        conn.commit()


## UserVerification
def get_user_by_email(conn, email):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = %s;
""", (email,))
        result = cur.fetchone()
        return  result
    