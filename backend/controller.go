package main
import(
	"net/http"

    "github.com/gin-gonic/gin"
)

func GetAllUserInformations(c *gin.Context) {
    var userinformations []Userinformations
    rows, err := db.Query("SELECT id, nickname, email, password FROM userinformations")
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    defer rows.Close()

    for rows.Next() {
        var userinformation Userinformations
        if err := rows.Scan(&userinformation.ID, &userinformation.Nickname, &userinformation.Email, &userinformation.Password); err != nil {
            c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
            return
        }
        userinformations = append(userinformations, userinformation)
    }

    c.JSON(http.StatusOK, userinformations)
}