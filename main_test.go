package main

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/gorilla/mux"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
    "secret-santa/models"      // Replace with your actual module path
    "secret-santa/routes"      // Replace with your actual module path
)

func setupTestDB() (*gorm.DB, func()) {
    // Use an in-memory SQLite database for testing
    db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
    if err != nil {
        panic("failed to connect database")
    }

    // Migrate the schema
    db.AutoMigrate(&models.User{}, &models.Group{}, &models.Assignment{})

    // Return cleanup function to close the database
    cleanup := func() {
        sqlDB, _ := db.DB()
        sqlDB.Close()
    }
    return db, cleanup
}

func setupRouter(db *gorm.DB) *mux.Router {
    router := mux.NewRouter()
    routes.RegisterRoutes(router, db)
    return router
}

func TestGetUsers(t *testing.T) {
    db, cleanup := setupTestDB()
    defer cleanup()

    // Insert a mock user
    db.Create(&models.User{ID: "1", Name: "John Doe", Email: "johndoe@example.com"})

    router := setupRouter(db)

    req, _ := http.NewRequest("GET", "/users", nil)
    response := httptest.NewRecorder()
    router.ServeHTTP(response, req)

    if status := response.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    var users []models.User
    err := json.Unmarshal(response.Body.Bytes(), &users)
    if err != nil {
        t.Errorf("error decoding response body: %v", err)
    }

    if len(users) != 1 || users[0].Name != "John Doe" {
        t.Errorf("expected user not found or mismatch")
    }
}

func TestPutUser(t *testing.T) {
    db, cleanup := setupTestDB()
    defer cleanup()

    router := setupRouter(db)

    user := models.User{ID: "2", Name: "Jane Doe", Email: "janedoe@example.com"}
    userJSON, _ := json.Marshal(user)
    req, _ := http.NewRequest("PUT", "/users", bytes.NewBuffer(userJSON))
    req.Header.Set("Content-Type", "application/json")

    response := httptest.NewRecorder()
    router.ServeHTTP(response, req)

    if status := response.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    var createdUser models.User
    db.First(&createdUser, "id = ?", "2")

    if createdUser.Name != "Jane Doe" || createdUser.Email != "janedoe@example.com" {
        t.Errorf("user was not created correctly")
    }
}

func TestGetGroups(t *testing.T) {
    db, cleanup := setupTestDB()
    defer cleanup()

    // Insert a mock group
    db.Create(&models.Group{ID: "1", Name: "Test Group", CreatedAt: gorm.NowFunc()})

    router := setupRouter(db)

    req, _ := http.NewRequest("GET", "/groups", nil)
    response := httptest.NewRecorder()
    router.ServeHTTP(response, req)

    if status := response.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    var groups []models.Group
    err := json.Unmarshal(response.Body.Bytes(), &groups)
    if err != nil {
        t.Errorf("error decoding response body: %v", err)
    }

    if len(groups) != 1 || groups[0].Name != "Test Group" {
        t.Errorf("expected group not found or mismatch")
    }
}

func TestPostAssignment(t *testing.T) {
    db, cleanup := setupTestDB()
    defer cleanup()

    // Insert mock data for group and users
    db.Create(&models.User{ID: "1", Name: "John Doe", Email: "johndoe@example.com"})
    db.Create(&models.User{ID: "2", Name: "Jane Doe", Email: "janedoe@example.com"})
    db.Create(&models.Group{ID: "1", Name: "Test Group", CreatedAt: gorm.NowFunc()})

    router := setupRouter(db)

    assignment := models.Assignment{ID: "1", GroupID: "1", GiverID: "1", ReceiverID: "2", AssignedAt: gorm.NowFunc()}
    assignmentJSON, _ := json.Marshal(assignment)
    req, _ := http.NewRequest("POST", "/assignments", bytes.NewBuffer(assignmentJSON))
    req.Header.Set("Content-Type", "application/json")

    response := httptest.NewRecorder()
    router.ServeHTTP(response, req)

    if status := response.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
    }

    var createdAssignment models.Assignment
    db.First(&createdAssignment, "id = ?", "1")

    if createdAssignment.GiverID != "1" || createdAssignment.ReceiverID != "2" {
        t.Errorf("assignment was not created correctly")
    }
}
