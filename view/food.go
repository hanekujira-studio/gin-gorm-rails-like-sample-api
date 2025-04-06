package view

import (
	"gin-gorm-rails-like-sample-api/model/entity"

	"github.com/gin-gonic/gin"
)

type responseFoods struct {
	Foods []foodWithHealthiness `json:"foods"`
}

// RenderFoods render foods.
func RenderFoods(c *gin.Context, foods []*entity.Food) {
	c.JSON(200, responseFoods{Foods: convertToViewFoods(foods)})
}

// RenderFood render food.
func RenderFood(c *gin.Context, food *entity.Food) {
	foodWithHealthiness := foodWithHealthiness{
		ID:              food.ID,
		FoodName:        food.FoodName,
		FoodDescription: food.FoodDescription,
		Calories:        food.Calories,
		Healthiness:     food.Healthiness(),
	}
	c.JSON(200, foodWithHealthiness)
}
