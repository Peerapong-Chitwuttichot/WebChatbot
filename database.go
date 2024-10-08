// database.go
package main

import (
    "database/sql"
    "log"

    _ "github.com/mattn/go-sqlite3"
)

var db *sql.DB

func initDB() {
    var err error

    // สร้างหรือเชื่อมต่อกับฐานข้อมูล SQLite ชื่อ `webchatbot.db`
    db, err = sql.Open("sqlite3", "./webchatbot.db")
    if err != nil {
        log.Fatal("Error opening database: ", err)
    }

    // สร้างตาราง `users` ถ้ายังไม่มีอยู่ในฐานข้อมูล
    createTable := `
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        age INTEGER
    );`
    
    _, err = db.Exec(createTable)
    if err != nil {
        log.Fatal("Error creating table: ", err)
    }

    log.Println("Database initialized and table created (if not exists)")
}
