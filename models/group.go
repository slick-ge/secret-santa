package models

import "time"

type Group struct {
    ID          string    `gorm:"primaryKey"`
    Name        string    `gorm:"size:255"`
    Description *string
    CreatedAt   time.Time
}
