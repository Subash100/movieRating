from django.urls import path,include

from rest_framework.routers import DefaultRouter
#from .views import movie_list,movie_detail
from .views import (WatchListAV, WatchDetailAV,
                    StreamPlatformList, StreamPlatformDetail, StreamPlatformVS,
                    ReviewList, ReviewDetail, ReviewCreate, UserReview, WatchListGV)

router = DefaultRouter()
router.register('stream',StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    # path('list/',movie_list,name='movie_list'),
    # path('detail/<int:pk>/',movie_detail,name='movie_detail'),
    # path('list/', MovieList.as_view(), name='MovieList'),
    # path('detail/<int:pk>/', MovieDetail.as_view(), name='MovieDetail'),


    path('list/',WatchListAV.as_view(),name='list'),
    path('<int:pk>/',WatchDetailAV.as_view(),name='detail'),
    path('list2/', WatchListGV.as_view(), name='watchlist'),

    path('',include(router.urls)),

    #path('stream/',StreamPlatformList.as_view(),name='stream'),
    #path('stream/<int:pk>/',StreamPlatformDetail.as_view(),name='stream_detail'),



    # path('review/',ReviewList.as_view(),name='review-list'),
    # path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    # path('stream/<int:pk>/review-create',ReviewCreate.as_view(),name='reviews-create'),
    # path('stream/<int:pk>/review',ReviewList.as_view(),name='reviews'),
    # path('stream/review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),

    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='reviews-create'),
    path('<int:pk>/reviews/',ReviewList.as_view(),name='reviews'),
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),
    path('review/',UserReview.as_view(),name='user-review-detail'),






]