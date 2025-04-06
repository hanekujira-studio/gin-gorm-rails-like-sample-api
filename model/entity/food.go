package entity

import (
	"time"
)

// Food is food models property
type Food struct {
	ID              uint64 `gorm:"primary_key"`
	FoodName        string
	FoodDescription string
	Calories        uint
	CreatedAt       time.Time
	DeletedAt       *time.Time
}

// Healthiness calculate health rating of Food by calories.
func (food *Food) Healthiness() *string {
	if food.Calories < 100 {
		rank := "ダイエット向き"
		return &rank
	} else if food.Calories < 300 {
		rank := "ヘルシー"
		return &rank
	} else if food.Calories < 500 {
		rank := "普通"
		return &rank
	} else if food.Calories < 800 {
		rank := "高カロリー"
		return &rank
	}
	rank := "超高カロリー"
	return &rank
}
