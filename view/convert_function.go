package view

import "gin-gorm-rails-like-sample-api/model/entity"

func convertToViewShops(before []*entity.Shop) []shop {
	after := make([]shop, len(before))
	for i, p := range before {
		after[i] = convertToViewShop(p)
	}
	return after
}

func convertToViewShop(before *entity.Shop) shop {
	return shop{
		ID:              before.ID,
		ShopName:        before.ShopName,
		ShopDescription: before.ShopDescription,
	}
}

func convertToViewBooks(before []*entity.Book) []bookWithRank {
	after := make([]bookWithRank, len(before))
	for i, p := range before {
		after[i] = convertToViewBook(p)
	}
	return after
}

func convertToViewBook(before *entity.Book) bookWithRank {
	return bookWithRank{
		ID:              before.ID,
		BookName:        before.BookName,
		BookDescription: before.BookDescription,
		Sales:           before.Sales,
		Rank:            before.Rank(),
	}
}

func convertToViewFoods(before []*entity.Food) []foodWithHealthiness {
	after := make([]foodWithHealthiness, len(before))
	for i, p := range before {
		after[i] = convertToViewFood(p)
	}
	return after
}

func convertToViewFood(before *entity.Food) foodWithHealthiness {
	return foodWithHealthiness{
		ID:              before.ID,
		FoodName:        before.FoodName,
		FoodDescription: before.FoodDescription,
		Calories:        before.Calories,
		Healthiness:     before.Healthiness(),
	}
}
