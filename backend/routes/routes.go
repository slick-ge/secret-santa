package routes

import (
	"github.com/gorilla/mux"
	"gorm.io/gorm"
	"secret-santa/backend/controllers"
)

func RegisterRoutes(router *mux.Router, db *gorm.DB) {
	//HealthCHeck
	//router.HandleFunc("/healthcheck", controllers.HealthCHeck(db)).Methods("GET")
	// User Routes
	router.HandleFunc("/users", controllers.GetUsers(db)).Methods("GET")
	router.HandleFunc("/users", controllers.PutUser(db)).Methods("PUT")

	// Group Routes
	router.HandleFunc("/groups", controllers.GetGroups(db)).Methods("GET")
	router.HandleFunc("/groups", controllers.PutGroup(db)).Methods("PUT")

	// Assignment Routes
	router.HandleFunc("/assignments/{group_id}", controllers.GetAssignmentsByGroup(db)).Methods("GET") // Update for group-specific assignments
	router.HandleFunc("/assignments", controllers.PostAssignment(db)).Methods("POST")
}
