import sqlite3
from datetime import datetime

# Verbindung zur Datenbank
connector = sqlite3.connect("D:\\DataBase\\CalorieTracker_DB.sqlite")
cursor = connector.cursor()

# SQL-Abfrage
cursor.execute("SELECT Date FROM DailyCals WHERE User = ?", ("Andreas",))
rows = cursor.fetchall()

# Unpacken der Daten aus den Tupeln
unpacked_rows = [row[0].strip() for row in rows]
print("Ungeordnete Daten:", unpacked_rows)

# Konvertieren der Strings in datetime.date-Objekte
date_objects = [datetime.strptime(row, "%Y-%m-%d").date() for row in unpacked_rows]
print("Unsortierte Datumsobjekte:", date_objects)

# Sortieren der datetime.date-Objekte
sorted_date_objects = sorted(date_objects)
print("Sortierte Datumsobjekte:", sorted_date_objects)

# Wandle zurück in Strings, falls nötig
sorted_dates = [date.strftime("%Y-%m-%d") for date in sorted_date_objects]
print("Sortierte Datumsstrings:", sorted_dates)

# Schließen der Verbindung
connector.close()