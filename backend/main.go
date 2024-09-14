// main.go
package main

import (
     "github.com/gin-gonic/gin"
)

func main() {
    initDB() // เรียกใช้งานการเชื่อมต่อฐานข้อมูล

     router := gin.Default()
     router.GET("/users",GetAllUserInformations)
     
    
     router.Run(":8080") // รันเซิร์ฟเวอร์ที่พอร์ต 8080
}