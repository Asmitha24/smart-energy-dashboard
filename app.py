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
    return [{"Year": row[0], "Energy Consumption EJ": row[1]} for row in data]

# API Route to Get Data as JSON (Dynamic)
@app.route("/energy", methods=["GET"])
def energy_data():
    data = get_energy_data()
    return jsonify(data)

# Route to Show Graph and JSON Data Together (Dynamic Updates)
@app.route("/")
def show_graph():
    data = get_energy_data()  # Get updated data
    years = [row["Year"] for row in data]
    energy_values = [row["Energy Consumption EJ"] for row in data]

    # Ensure static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    # Delete old graph if it exists
    graph_path = "static/energy_plot.png"
    if os.path.exists(graph_path):
        os.remove(graph_path)

    # Generate New Graph
    plt.figure(figsize=(10, 5))
    plt.plot(years, energy_values, marker='o', linestyle='-', color='b')
    plt.xlabel("Year")
    plt.ylabel("Energy Consumption (EJ)")
    plt.title("Energy Consumption Over the Years")
    plt.grid()

    plt.savefig(graph_path)  # Save the new graph as an image
    plt.close()

    # Pass updated data to the template
    return render_template("index.html", energy_data=data)

if __name__ == "__main__":
    app.run(debug=True)
