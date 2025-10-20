import psycopg2
conn = psycopg2.connect(
 dbname="testdb",
 user="postgres",
 password="admin123",
 host="localhost",
 port="5432"
)
cur = conn.cursor()

# CREATE
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Анна", 30))
# READ
cur.execute("SELECT * FROM users;")
print("Все пользователи:", cur.fetchall())
# UPDATE
cur.execute("UPDATE users SET age = %s WHERE name = %s", (35, "Анна"))
# DELETE
cur.execute("DELETE FROM users WHERE name = %s", ("Анна",))


conn.commit()
cur.close()
conn.close()
