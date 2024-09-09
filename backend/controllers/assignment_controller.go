package controllers

import (
	"encoding/json"
	"github.com/gorilla/mux"
	"gorm.io/gorm"
	"net/http"
	"secret-santa/backend/models"
)

func GetAssignmentsByGroup(db *gorm.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)
		groupID := vars["group_id"]

		var assignments []models.Assignment
		if result := db.Preload("Group").Preload("Giver").Preload("Receiver").Where("group_id = ?", groupID).Find(&assignments); result.Error != nil {
			http.Error(w, result.Error.Error(), http.StatusInternalServerError)
			return
		}

		if len(assignments) == 0 {
			http.Error(w, "No assignments found for the specified group", http.StatusNotFound)
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
