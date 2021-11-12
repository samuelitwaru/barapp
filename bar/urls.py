from django.urls import path
from .api import *
from .views import *


app_name = "bar"


router = routers.DefaultRouter()
router.register('metrics', MetricViewSet)
router.register('metric-systems', MetricSystemViewSet)
router.register('orders', OrderViewSet)
router.register('products', ProductViewSet)
router.register('profiles', ProfileViewSet)
router.register('sale-guides', SaleGuideViewSet)
router.register('stock', StockViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
	url(r'^api/', include(router.urls)),
	path('', index, name='index'),
	path('login', login_view, name='login'),
	path('logout', logout_view, name='logout'),
	
	path('orders', orders, name='orders'),
	path('orders/create', create_orders, name='create_orders'),
	path('orders/update/status', update_order_status, name='update_order_status'),
	
	path('profiles', get_profiles, name='get_profiles'),
	path('profiles/<int:id>', get_profile, name='get_profile'),

	path('profile', get_current_user_profile, name='get_current_user_profile'),
	path('profile/update', update_current_user_profile, name='update_current_user_profile'),
	path('profile/password/update', update_current_user_password, name='update_current_user_password'),

	path('users', UsersPageView.as_view(), name='get_users'),
	path('users/create', create_user, name='create_user'),
	path('users/<int:id>', update_user, name='update_user'),
	path('users/<int:id>/permissions/update', update_user_permissions, name='update_user_permissions'),


	path('metric-systems', MetricSystemsPageView.as_view(), name='get_metric_systems'),
	path('metric-systems/create', create_metric_system, name='create_metric_system'),

	# path('users/<pk>/', UserDetailView.as_view(), name='get_user'),
	# path('metric-systems/<pk>/', MetricSystemDetailView.as_view(), name='get_metric_system'),
	path('products', ProductsPageView.as_view(), name='get_products'),
	path('products/create', create_product, name='create_product'),
	# path('products/<pk>/', ProductDetailView.as_view(), name='get_product'),
	path('products/<int:id>/', get_product, name='get_product'),
	path('products/<int:id>/purchasing/update', update_product_purchasing, name='update_product_purchasing'),
	path('products/<int:id>/categories/update', update_product_categories, name='update_product_categories'),

	path('categories/create', create_category, name='create_category'),
	path('categories/<int:id>/', get_category, name='get_category'),
]
