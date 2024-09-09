package models

import "time"

type Assignment struct {
	ID         string `gorm:"primaryKey"`
	GroupID    string
	GiverID    string
	ReceiverID string
	AssignedAt time.Time

	Group    Group `gorm:"foreignKey:GroupID"`
	Giver    User  `gorm:"foreignKey:GiverID"`
	Receiver User  `gorm:"foreignKey:ReceiverID"`
}
