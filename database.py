import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
def connect_db():
    return sqlite3.connect('chatbot_history.db')

# Create a table to store chat history
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            chat_history TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save chat history to the database
def save_chat_to_db(file_name, chat_history):
    conn = connect_db()
    cursor = conn.cursor()

    # Convert chat history to a single string
    chat_history_str = '\n'.join(
        [f"User: {entry['content']}" if entry['role'] == 'user' else f"Bot: {entry['content']}" for entry in chat_history]
    )

    # Insert data into the database
    cursor.execute('''
        INSERT INTO chat_history (file_name, chat_history)
        VALUES (?, ?)
    ''', (file_name, chat_history_str))

    conn.commit()
    conn.close()

# Retrieve chat history for a specific file
def get_chat_history(file_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT chat_history FROM chat_history WHERE file_name = ?
    ''', (file_name,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] if result else None

# Initialize the database
create_table()
