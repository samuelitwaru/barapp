from django.urls import path
from .api import *
from .views import *
from django.views.generic import TemplateView


app_name = "bar"


router = routers.DefaultRouter()
router.register('metrics', MetricViewSet)
router.register('metric-systems', MetricSystemViewSet)
router.register('orders', OrderViewSet)
router.register('order-groups', OrderGroupViewSet)
router.register('products', ProductViewSet)
router.register('profiles', ProfileViewSet)
router.register('sale-guides', SaleGuideViewSet)
router.register('stock', StockViewSet)
router.register('categories', CategoryViewSet)


urlpatterns = [
	url(r'^api/', include(router.urls)),
	path('', index, name='index'),
	path('home', TemplateView.as_view(template_name='pages/trial.html'), name='index'),
	path('login', login_view, name='login'),
	path('login/waiter/<int:id>', login_waiter, name='login_waiter'),
	path('logout', logout_view, name='logout'),
	
	path('orders', orders, name='orders'),
	path('orders/create', create_orders, name='create_orders'),
	# path('orders/update/<int:order_group_id>', update_orders, name='update_orders'),
	path('orders/update/status', update_order_status, name='update_order_status'),
	path('orders/sales', get_order_sales, name='get_order_sales'),
	
	path('order-groups', get_order_groups, name='get_order_groups'),
	path('order-groups/<int:id>', get_order_group, name='get_order_group'),
	path('order-groups/<int:id>/update', update_order_group, name='update_order_group'),
	path('order-groups/<int:id>/open-or-close', open_or_close_order_group, name='open_or_close_order_group'),
	path('order-groups/<int:id>/delete', delete_order_group, name='delete_order_group'),
	
	path('purchases', get_purchases, name='get_purchases'),

	path('profile', get_current_user_profile, name='get_current_user_profile'),
	path('profile/update', update_current_user_profile, name='update_current_user_profile'),
	path('profile/password/update', update_current_user_password, name='update_current_user_password'),

	path('profiles', get_profiles, name='get_profiles'),
	path('profiles/<int:id>', get_profile, name='get_profile'),
	path('users/create', create_user, name='create_user'),
	path('users/<int:id>', update_user, name='update_user'),
	path('users/<int:id>/delete', delete_user, name='delete_user'),
	path('users/<int:id>/password/update', update_user_password, name='update_user_password'),
	path('users/<int:id>/permissions/update', update_user_permissions, name='update_user_permissions'),


	path('metric-systems', MetricSystemsPageView.as_view(), name='get_metric_systems'),
	path('metric-systems/create', create_metric_system, name='create_metric_system'),
	path('metric-systems/<int:id>/delete', delete_metric_system, name='delete_metric_system'),

	path('products', get_products, name='get_products'),
	path('products/create', create_product, name='create_product'),
	path('products/<int:id>/', get_product, name='get_product'),
	path('products/<int:id>/purchasing/update', update_product_purchasing, name='update_product_purchasing'),
	path('products/<int:id>/delete', delete_product, name='delete_product'),
	path('products/<int:id>/categories/update', update_product_categories, name='update_product_categories'),
	path('products/<int:id>/stock/add', add_product_stock, name='add_product_stock'),

	path('categories/create', create_category, name='create_category'),
	path('categories/<int:id>/', get_category, name='get_category'),
	path('categories/<int:id>/delete', delete_category, name='delete_category'),

	path('notifications', get_notifications, name='get_notifications'),
	path('notifications/count', get_notification_count, name='get_notification_count'),

]
