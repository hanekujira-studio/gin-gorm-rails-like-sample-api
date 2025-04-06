package model

import (
	"gin-gorm-rails-like-sample-api/db"
	"gin-gorm-rails-like-sample-api/model/entity"

	"github.com/gin-gonic/gin"
)

// GetFoodAll is get all Food
func GetFoodAll() ([]*entity.Food, error) {
	db := db.GetDB()
	var u []*entity.Food
	if err := db.Find(&u).Error; err != nil {
		return nil, err
	}

	return u, nil
}

// GetFoodByID is get a Food
func GetFoodByID(id string) (*entity.Food, error) {
	db := db.GetDB()
	var u entity.Food
	if err := db.Where("id = ?", id).First(&u).Error; err != nil {
		return &u, err
	}

	return &u, nil
}

// CreateFood is create Food model
func CreateFood(c *gin.Context) (*entity.Food, error) {
	db := db.GetDB()
	var u entity.Food

	if err := c.BindJSON(&u); err != nil {
		return nil, err
	}

	if err := db.Create(&u).Error; err != nil {
		return nil, err
	}

	return &u, nil
}

// UpdateFoodByID is update a Food
func UpdateFoodByID(id string, c *gin.Context) (*entity.Food, error) {
	db := db.GetDB()
	var u entity.Food

	if err := db.Where("id = ?", id).First(&u).Error; err != nil {
		return nil, err
	}

	if err := c.BindJSON(&u); err != nil {
		return nil, err
	}

	db.Save(&u)

	return &u, nil
}

// DeleteFoodByID is delete a Food
func DeleteFoodByID(id string) error {
	db := db.GetDB()
	var u entity.Food

	if err := db.Where("id = ?", id).Delete(&u).Error; err != nil {
		return err
	}

	return nil
}
