from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = router.urls

# URLConf
# We use this if we still need to include some other url pathes
# urlpatterns = [
#     Including the router urls at first:
#     path('', include(router.urls))
#     Adding other url pathes:
#     path('products/', views.ProductList.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
#     path('collections/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),
# ]
