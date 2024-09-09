package main

import (
	"github.com/gorilla/mux"
    "gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"net/http"
	"secret-santa/backend/models"
	"secret-santa/backend/routes"
)

var db *gorm.DB


func main() {

	initDB()

	// Auto migrate models
	db.AutoMigrate(&models.User{}, &models.Group{}, &models.Assignment{})

	// Initialize router
	router := mux.NewRouter()

	// Register routes
	routes.RegisterRoutes(router, db)

	// Start server
	log.Println("Server listening on port 8080")
	log.Fatal(http.ListenAndServe(":8080", router))
}

func initDB() {
	var err error
	dsn := "host=localhost user=youruser password=yourpassword dbname=yourdb port=5432 sslmode=disable"
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
}