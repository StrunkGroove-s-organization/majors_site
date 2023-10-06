from django.urls import path
from . import views

urlpatterns = [
    path(
        'links_without_cards/', 
        views.LinksWithoutCardsView.as_view(), 
        name='links_without_cards'
    ),
    path(
        'mezhbirzhevye-svyazki/', 
        views.MezhbirzhevyeSvyazkiView.as_view(), 
        name='mezhbirzhevye_svyazki'
    ),
    path('api/v1/links_without_cards_3/', views.PriceViewThree.as_view()),
    path('api/v1/mezhbirzhevye-svyazki/', views.PriceViewTwo.as_view()),
    path('api/v1/favorite-without-2/', views.FavouriteTwoView.as_view()),
    path('api/v1/favorite-without-3/', views.FavouriteThreeView.as_view()),
    path('api/v1/get-info-best-change/', views.GetInfoBestChange.as_view()),
]
