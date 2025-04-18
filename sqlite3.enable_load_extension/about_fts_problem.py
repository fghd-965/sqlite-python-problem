import sqlite3, sys, os

# Database file path
db_path = "tutorial.db"

# Connecting to a SQLite Database
con = sqlite3.connect(db_path)

# ---------------------------------------------------------
# Comment out or delete the following code block that loads the extension
# Modern Python's sqlite3 usually has FTS functionality built in.
# ---------------------------------------------------------
# # Path to your fts3.so file. Very important!
# fts_path = r"D:\Standard Library ( Python)\Crawler Framework\about_sqlite3\fts3.so" # Or it should be .dll
#
# # 2. Enable loading extensions
# con.enable_load_extension(True)
#
# # 3. Try to load the FTS extension
# try:
#     con.execute(f"select load_extension('{fts_path}')")
#     print("FTS extension loaded successfully!")
# except sqlite3.OperationalError as e:
#     print(f"Failed to load FTS extension: {e}")
#     print("Make sure fts_path points to the correct FTS extension file (.dll for Windows), and that the file exists and the architecture matches Python.")
#     print("Also check if there are any missing dependency DLL files (Windows)")
#     print("Usually, modern Python's sqlite3 has FTS built in, no need to load manually.")
#     sys.exit(1)  # Extension loading failed, exit the program to avoid subsequent errors
#
# # 4. Disable loading extensions (for security, disable after loading)
# con.enable_load_extension(False)
# ---------------------------------------------------------

# 5. Delete the existing recipe table (if it exists) - suitable for development/testing environments
con.execute("DROP TABLE IF EXISTS recipe")

# 6. Create a virtual table recipe (try using FTS3 directly)
try:
    con.execute("CREATE VIRTUAL TABLE recipe USING fts3(name, ingredients)")
    print("FTS virtual table created successfully!")
except sqlite3.OperationalError as e:
    print(f"Failed to create FTS virtual table: {e}")
    print("It seems that your Python sqlite3 module may not have built-in FTS3 support.")
    print("Please refer to the 'Alternative Solution' below.")
    con.close()
    sys.exit(1)


# 7. Insert some data
con.executescript("""
    INSERT INTO recipe (name, ingredients) VALUES('broccoli stew', 'broccoli peppers cheese tomatoes');
    INSERT INTO recipe (name, ingredients) VALUES('broccoli stew', 'broccoli onions gralic celery');
    INSERT INTO recipe (name, ingredients) VALUES('broccoli pie', 'broccoli cheese onions flour');
    INSERT INTO recipe (name, ingredients) VALUES('broccoli pie', 'pumpkin sugar flour butter');
    """)

# 8. Query data
print("Recipes where name contains 'pie':")
for row in con.execute("SELECT rowid, name FROM recipe WHERE name MATCH 'pie'"):
    print(row)

# 9. Close the database connection
con.close()

print("Program running ends")
