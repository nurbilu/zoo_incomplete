from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)

def create_connection():
    return sqlite3.connect("animals.db")

# Function to create the animals table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            origin TEXT NOT NULL,
            picture TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
# Initialize the database and table
create_table()

@app.route("/")
def home():
    return render_template("home.html")

# CRUD

@app.route("/show_animals", methods=["GET", "POST"])
def show_animals():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animals")
    animals = cursor.fetchall()
    conn.close()

    return render_template("animals.html", animals=animals)


@app.route("/add_animal", methods=["GET", "POST"])
def add_animal():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        origin = request.form['origin']
        picture = request.form['picture']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO animals (name, age, origin, picture) VALUES (?, ?, ?, ?)", (name, age, origin, picture))
        conn.commit()
        conn.close()
        return redirect(url_for('show_animals'))
    return render_template("add_animal.html")

    
@app.route('/edit_animal/', methods=["GET", "POST"])
@app.route('/edit_animal/<int:animal_id>', methods=["GET", "POST"])
def edit_animal(animal_id=None):
    conn = create_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        origin = request.form['origin']
        picture = request.form['picture']

        if animal_id is not None:
            # Update the record in the database for the specified car ID
            cursor.execute("UPDATE animals SET name=?, age=?, origin=?, picture=? WHERE id=?", (name, age, origin, picture, animal_id))
        else:
            # Insert a new record in the database if no car ID is provided
            cursor.execute("INSERT INTO animals (name, age, origin, picture) VALUES (?, ?, ?, ?)", (name, age, origin, picture))

        conn.commit()
        conn.close()

        return redirect(url_for('show_animals'))

    else:
        if animal_id is not None:
            # Fetch the car information to pre-fill the form for the specified car ID
            cursor.execute("SELECT * FROM animals WHERE id=?", (animal_id,))
            car = cursor.fetchone()
            conn.close()

            if car:
                return render_template("edit_ani.html", animal=animal)
            else:
                return "animal not found"
        else:
            # Render the update form without pre-filled information for a new car
            conn.close()
            return render_template("edit_ani.html", animal=None)

    
    
@app.route("/delete_animal/<int:animal_id>", methods=["GET", "POST"])
def delete_animal(animal_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM animals WHERE id=?", (animal_id))
    conn.commit()
    conn.close()
    return redirect(url_for('show_animals'))



if __name__ == "__main__":
    app.run(debug=True,port=8080)