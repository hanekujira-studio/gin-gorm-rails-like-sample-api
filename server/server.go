package server

import (
	"gin-gorm-viron/controller"

	"github.com/gin-gonic/gin"
)

// Init is initialize server
func Init() {
	r := router()
	r.Run()
}

func router() *gin.Engine {
	r := gin.Default()

	users := r.Group("/users")
	{
		ctrl := controller.UserController{}
		users.GET("", ctrl.IndexUser)
		users.GET("/:id", ctrl.ShowUser)
		users.POST("/", ctrl.CreateUser)
		users.PUT("/:id", ctrl.UpdateUser)
		users.DELETE("/:id", ctrl.DeleteUser)
	}

	swagger := r.Group("/")
	{
		ctrl := controller.SwaggerController{}
		swagger.GET("/swagger.json", ctrl.ShowSwagger)
	}
	return r
}
