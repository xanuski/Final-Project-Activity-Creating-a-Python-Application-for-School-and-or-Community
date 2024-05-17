from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'db.sqlite3'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            skills TEXT NOT NULL,
            time_commitment TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            skills TEXT NOT NULL,
            availability TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def lead():
    return render_template('lead.html')

@app.route('/chance', methods=['GET', 'POST'])
def chance():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    if request.method == 'POST':
        search_query = request.form['search']
        cursor.execute('SELECT * FROM opportunities WHERE title LIKE ? OR description LIKE ? OR skills LIKE ?',
                       ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute('SELECT * FROM opportunities')
    
    opportunities = cursor.fetchall()
    conn.close()
    return render_template('chance.html', opportunities=opportunities)

@app.route('/opportunity/<int:opportunity_id>')
def opportunity_detail(opportunity_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM opportunities WHERE id = ?', (opportunity_id,))
    opportunity = cursor.fetchone()
    conn.close()
    return render_template('opportunity_detail.html', opportunity=opportunity)

@app.route('/participants', methods=['GET', 'POST'])
def participants():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        skills = request.form['skills']
        availability = request.form['availability']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO volunteers (name, email, skills, availability) VALUES (?, ?, ?, ?)',
                       (name, email, skills, availability))
        conn.commit()
        conn.close()
        return redirect(url_for('lead'))
    return render_template('participants.html')

@app.route('/create_opportunity', methods=['GET', 'POST'])
def create_opportunity():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        skills = request.form['skills']
        time_commitment = request.form['time_commitment']
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO opportunities (title, description, skills, time_commitment) VALUES (?, ?, ?, ?)',
                       (title, description, skills, time_commitment))
        conn.commit()
        conn.close()
        return redirect(url_for('chance'))
    return render_template('create_opportunity.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
