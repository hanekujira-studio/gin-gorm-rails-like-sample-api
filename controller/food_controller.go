package controller

import (
	"fmt"
	"gin-gorm-rails-like-sample-api/model"
	"gin-gorm-rails-like-sample-api/view"

	"github.com/gin-gonic/gin"
)

// FoodController is food controlller
type FoodController struct{}

// IndexFood action: GET /foods
func (pc FoodController) IndexFood(c *gin.Context) {
	foods, err := model.GetFoodAll()

	if err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	} else {
		view.RenderFoods(c, foods)
	}
}

// CreateFood action: POST /foods
func (pc FoodController) CreateFood(c *gin.Context) {
	_, err := model.CreateFood(c)

	if err != nil {
		c.AbortWithStatus(400)
		fmt.Println(err)
	} else {
		c.JSON(204, nil)
	}
}

// ShowFood action: GET /foods/:id
func (pc FoodController) ShowFood(c *gin.Context) {
	id := c.Params.ByName("id")
	food, err := model.GetFoodByID(id)

	if err != nil {
		c.AbortWithStatus(404)
		fmt.Println(err)
	} else {
		view.RenderFood(c, food)
	}
}

// UpdateFood action: PUT /foods/:id
func (pc FoodController) UpdateFood(c *gin.Context) {
	id := c.Params.ByName("id")
	food, err := model.UpdateFoodByID(id, c)

	if err != nil {
		c.AbortWithStatus(400)
		fmt.Println(err)
	} else {
		view.RenderFood(c, food)
	}
}

// DeleteFood action: DELETE /foods/:id
func (pc FoodController) DeleteFood(c *gin.Context) {
	id := c.Params.ByName("id")

	if err := model.DeleteFoodByID(id); err != nil {
		c.AbortWithStatus(403)
		fmt.Println(err)
	} else {
		c.JSON(204, nil)
	}
}
