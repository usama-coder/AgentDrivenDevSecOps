```python
def sqlQuery():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = input("Enter username: ")
    query = "SELECT * FROM users WHERE username = %s;"
    cursor.execute(query, (username,))
```