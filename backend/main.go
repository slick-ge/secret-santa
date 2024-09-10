package main

import (
	"github.com/gorilla/mux"
    "gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"net/http"
	"secret-santa/backend/models"
	"secret-santa/backend/routes"
	"os"
	"fmt"
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

	dbHost := os.Getenv("DB_HOST")
	dbPort := os.Getenv("DB_PORT")
	dbUser := os.Getenv("DB_USER")
	dbPassword := os.Getenv("DB_PASSWORD")
	dbName := os.Getenv("DB_NAME")

	var err error

	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable", dbHost, dbUser, dbPassword, dbName, dbPort)
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
}