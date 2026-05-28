from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Деректер базасын автоматты түрде құру функциясы
def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            contact TEXT NOT NULL,
            desc TEXT,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ИИ Логикасы: Кітаптың атына қарап санатты анықтау
def predict_category(title):
    title_lower = title.lower()
    categories = {
        "Бағдарламалау мен АТ": ["c++", "python", "java", "код", "программирование", "it", "веб", "кибер", "security"],
        "Математика": ["математика", "алгебра", "геометрия", "дискретті", "талдау", "анализ"],
        "Тілдер": ["ағылшын", "english", "корей", "қазақ", "орыс", "сөздік"],
        "Көркем әдебиет": ["роман", "кітап", "әңгіме", "повесть", "психология", "абай", "жолы", "мотивация"]
    }
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "Жалпы білім / Basqa"

@app.route('/')
def index():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    rows = cursor.execute('SELECT title, price, contact, desc, category FROM books ORDER BY id DESC').fetchall()
    conn.close()
    
    books = []
    for row in rows:
        books.append({
            "title": row[0], "price": row[1], "contact": row[2], "desc": row[3], "category": row[4]
        })
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    price = request.form.get('price')
    contact = request.form.get('contact')
    desc = request.form.get('desc')
    predicted_cat = predict_category(title)
    
    if title and price and contact:
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, price, contact, desc, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, price, contact, desc, predicted_cat))
        conn.commit()
        conn.close()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)