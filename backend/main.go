package main

import (
	"github.com/gorilla/mux"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"
	"net/http"
	"secret-santa/backend/models"
	"secret-santa/backend/routes"
)

func main() {
	// Initialize DB connection
	db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("failed to connect database: ", err)
	}

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
