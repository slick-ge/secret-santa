package models

import "time"

type User struct {
	ID            string `gorm:"primaryKey"`
	Name          string `gorm:"size:255"`
	Email         string `gorm:"unique"`
	EmailVerified *time.Time
	Image         *string
}
