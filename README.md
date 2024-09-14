# WebChatbot

Step Setup Project

Create Project Webchatbot
1.โหลด Go และติดตั้ง
2. cd WebChatbot --> go mod init WebChatbot เพื่อสร้าง go.mod
3. cd WebChatbot --> go get -u github.com/gin-gonic/gin
  cd WebChatbot --> go get github.com/mattn/go-sqlite3 (ถ้าใช้ MySQL go get github.com/go-sql-driver/mysql)


WebChatbot/
├── main.go
├── handlers.go
├── database.go
├── models.go
├── go.mod
└── README.md

ใช้ cd WebChatbot --> go run main.go handlers.go database.go models.go เพื่อ Build และ Run โปรเจค

ใช้ Postman สำหรับ GET // Post
