# notes_database

This container hosts a SQLite database used for schema parity and data inspection alongside the mobile app. The Flutter app itself uses an on-device SQLite database at runtime and does not connect to this container. Both instances maintain the same notes table schema so you can seed and inspect data here while the app persists notes locally.

## What This Container Provides

This repository includes helper scripts to initialize and explore a SQLite database:
- init_db.py: Creates myapp.db and ensures required tables exist; seeds sample notes if empty.
- db_shell.py: A simple interactive SQLite shell for quick inspection.
- db_visualizer/: A minimal Node.js viewer capable of browsing tables for multiple database types; configured for SQLite via sqlite.env.
- backup_db.sh and restore_db.sh: Utilities for backing up and restoring the database file.

Database file path after initialization:
- notes_database/myapp.db

## Initialize the Database

From this directory:

```bash
python3 init_db.py
```

This script creates myapp.db if it does not exist, ensures tables are present, and writes connection information to db_connection.txt. It also writes db_visualizer/sqlite.env that points to the absolute path of myapp.db.

To verify the schema and basic connectivity:

```bash
python3 test_db.py
```

A successful run prints the SQLite version, confirms the notes table exists with required columns, and shows how many rows are present.

## Inspect the Database

Option 1: Use the built-in interactive shell:

```bash
python3 db_shell.py
```

Helpful commands within the shell:
- .tables to list tables
- .schema [table] to print the CREATE statement
- .describe [table] to view columns and types
- .quit to exit

Option 2: Use the sqlite3 CLI (if available on your machine):

```bash
sqlite3 myapp.db
```

Option 3: Use the simple Node.js viewer:
1) Ensure Node.js is installed.
2) Source the generated sqlite.env to set the SQLITE_DB path:
```bash
source db_visualizer/sqlite.env
```
3) Start the viewer:
```bash
cd db_visualizer
npm install
npm start
```
4) Open http://localhost:3000 in a browser and select the SQLite option.

## Schema Parity With Mobile App

Both the mobile app and this container use the same notes schema:

- Table name: notes
- Columns:
  - id INTEGER PRIMARY KEY AUTOINCREMENT
  - title TEXT NOT NULL
  - content TEXT NOT NULL
  - created_at INTEGER
  - updated_at INTEGER

This is implemented here in init_db.py and mirrored in the mobile app (lib/data/database_helper.dart). While you can seed or inspect data via this container, the Flutter app reads and writes to its own device-local database and does not synchronize with this file automatically.

## Backup and Restore

Create a backup of the SQLite file:

```bash
./backup_db.sh
```

This produces database_backup.db in the same directory.

Restore from a backup:

```bash
./restore_db.sh
```

If database_backup.db exists it will replace myapp.db.

## Notes and Tips

- No network linkage: The mobile app does not connect to this container at runtime. Treat this database as a parity reference and an inspection aid.
- Sample data: init_db.py seeds two example notes if the notes table is empty. Rerunning init_db.py is idempotent for schema and will not duplicate seeds when rows already exist.
- Location reference: db_connection.txt contains a connection string and absolute file path to myapp.db for quick tooling configuration.
