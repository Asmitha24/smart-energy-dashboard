import os
from flask import Flask, jsonify, render_template
import sqlite3
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to fetch data from SQLite
def get_energy_data():
    conn = sqlite3.connect("energy_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT Year, SUM(`Energy Consumption EJ`) FROM energy_usage GROUP BY Year")  
    data = cursor.fetchall()
    
    conn.close()
    return data

# API Route to Get Data as JSON
@app.route("/energy", methods=["GET"])
def energy_data():
    data = get_energy_data()
    return jsonify(data)

# Route to Generate and Display Graph
@app.route("/")
def show_graph():
    data = get_energy_data()
    years = [row[0] for row in data]
    energy_values = [row[1] for row in data]

    # Ensure static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure(figsize=(10, 5))
    plt.plot(years, energy_values, marker='o', linestyle='-', color='b')
    plt.xlabel("Year")
    plt.ylabel("Energy Consumption (EJ)")
    plt.title("Energy Consumption Over the Years")
    plt.grid()

    plt.savefig("static/energy_plot.png")  # Save the graph as an image
    plt.close()  # Close the plot to free memory

    return render_template("index.html")  # Render the webpage

if __name__ == "__main__":
    app.run(debug=True)
