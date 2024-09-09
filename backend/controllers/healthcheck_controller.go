package controllers

import (
	"encoding/json"
	"net/http"
	"secret-santa/backend/models"
    "github.com/gorilla/mux"
	"gorm.io/gorm"
)

func HealthCHeck(db *gorm.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		pingErr := db.DB().Ping()
		if pingErr != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		} else {
			http.Error(w, result.Error.Error(), http.StatusInternalServerError)
			return
		}
		json.NewEncoder(w).Encode(healthcheck)
	}
}
