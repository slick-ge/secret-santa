package controllers

import (
	"encoding/json"
	"net/http"
	"secret-santa/models"
	"gorm.io/gorm"
)

func GetAssignments(db *gorm.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var assignments []models.Assignment
		if result := db.Preload("Group").Preload("Giver").Preload("Receiver").Find(&assignments); result.Error != nil {
			http.Error(w, result.Error.Error(), http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(assignments)
	}
}

func PostAssignment(db *gorm.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var assignment models.Assignment
		if err := json.NewDecoder(r.Body).Decode(&assignment); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		if result := db.Create(&assignment); result.Error != nil {
			http.Error(w, result.Error.Error(), http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(assignment)
	}
}
