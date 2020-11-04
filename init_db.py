import sqlite3

def first_execute():
    conn = sqlite3.connect('database.db')
    conn.execute('DROP TABLE IF EXISTS people')
    conn.execute('''
    		CREATE TABLE IF NOT EXISTS people(
    			id INTEGER PRIMARY KEY AUTOINCREMENT,
    			name TEXT VARCHAR(30),
    			email TEXT VARCHAR(50),
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                title TEXT NOT NULL UNIQUE,
    			content TEXT UNIQUE
    		)
            ''')
    
    cursor = conn.cursor()
    cursor.execute('INSERT INTO people (name, email, title, content) VALUES (?, ?, ?, ?)',
    				('Darley', 'tiusdiux.com@gmail.com', 'First Post', 'Content for the First Post'))
    cursor.execute('INSERT INTO people (name, email, title, content) VALUES (?, ?, ?, ?)',
    				('Darley', 'tiusdiux.com@gmail.com', 'Second Post','Content for the Second Post'))
    conn.commit()
    conn.close()
