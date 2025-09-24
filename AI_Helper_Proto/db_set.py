import sqlite3

conn = sqlite3.connect("stardewValley.db")
cursor = conn.cursor()


cursor.execute("SELECT name, season FROM crops")

results = cursor.fetchall()

print("所有农作物及其季节:")
for row in results:
    print(row)

conn.close()