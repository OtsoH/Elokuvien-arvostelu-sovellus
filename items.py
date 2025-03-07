import db

def get_all_classes():
    sql = """SELECT title, value FROM classes ORDER BY id"""
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes


def add_item(title, description, user_id, classes):
    sql = """INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"""
    db.execute(sql, [title, description, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def get_classes(item_id):
    sql = """SELECT title, value FROM item_classes WHERE item_id = ?"""
    return db.query(sql, [item_id])   

def get_items():
    sql = """SELECT items.id, items.title, users.id AS user_id, users.username, COUNT(comments.id) comments_count
                FROM items 
                JOIN users ON items.user_id = users.id
                LEFT JOIN comments ON items.id = comments.item_id
                GROUP BY items.id
                ORDER BY items.id DESC"""
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title,
                    items.id,
                    items.description,
                    users.id user_id,
                    users.username        
             FROM items, users
             WHERE items.user_id = users.id AND
                   items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None
    

def update_item(item_id, title, description, classes):
    sql = """UPDATE items SET title = ?, description = ? WHERE id = ?"""
    db.execute(sql, [title, description, item_id])

    sql = """DELETE FROM item_classes WHERE item_id = ?"""
    db.execute(sql, [item_id])

    sql = """INSERT INTO item_classes (item_id, title, value) VALUES (?,?,?)"""
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def delete_item(item_id):
    sql = "DELETE FROM comments WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = """DELETE FROM item_classes WHERE item_id = ?"""
    db.execute(sql, [item_id])

    sql = """DELETE FROM items WHERE id = ?"""
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title
             FROM items
             WHERE title LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])

def add_comment(item_id, user_id, comment):
    sql = """INSERT INTO comments (item_id, user_id, comment) VALUES (?, ?, ?)"""
    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql = """SELECT comments.comment, users.id AS user_id, users.username
             FROM comments
             JOIN users ON comments.user_id = users.id
             WHERE comments.item_id = ?
             ORDER BY comments.id DESC"""
    return db.query(sql, [item_id])