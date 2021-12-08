from django.db import models
from django.contrib.auth.models import User
from .utils import STATUS_CHOICES, PENDING, PAID


# Create your models here.
class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class MetricSystem(TimeStampedModel):
	name = models.CharField(max_length=128)
	is_standard = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def base_metric(self):
		return self.metric_set.filter(multiplier=1.0).first()

	def convert(self, quantity, from_metric, to_metric):
		return quantity*(to_metric.multiplier/from_metric.multiplier)


class Metric(TimeStampedModel):
	unit = models.CharField(max_length=128)
	symbol = models.CharField(max_length=64)
	multiplier = models.FloatField()
	metric_system = models.ForeignKey(MetricSystem, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.unit} {self.symbol}"


class Product(TimeStampedModel):
	name = models.CharField(max_length=128)
	brand = models.CharField(max_length=128)
	description = models.CharField(max_length=2048, null=True)
	barcode = models.CharField(max_length=128, null=True, unique=True)
	quantity = models.FloatField(default=0)
	stock_limit = models.FloatField(default=0)
	purchase_price = models.IntegerField(null=True)
	metric_system = models.ForeignKey(MetricSystem, on_delete=models.CASCADE)
	purchase_metric = models.ForeignKey(Metric, null=True, on_delete=models.SET_NULL)
	categories = models.ManyToManyField('Category', through='ProductCategories', through_fields=('product', 'category'))

	def __str__(self):
		return self.name

	def stock_value(self):
		quantity_in_default_sale_guide_metric = 0
		default_sale_guide = self.sale_guides.first()
		if default_sale_guide and self.purchase_metric:
			quantity_in_default_sale_guide_metric = self.metric_system.convert(self.quantity, self.purchase_metric, default_sale_guide.metric)
			return quantity_in_default_sale_guide_metric * default_sale_guide.price

	def update_quantity_by(self, quantity, metric):
		if self.purchase_metric!=metric:
			quantity = self.metric_system.convert(quantity, metric, self.purchase_metric)
		self.quantity += quantity
		self.save()

	def convert_quantities(self, old_purchase_metric, new_purchase_metric):
		quantity = self.metric_system.convert(self.quantity, old_purchase_metric, new_purchase_metric)
		stock_limit = self.metric_system.convert(self.stock_limit, old_purchase_metric, new_purchase_metric)
		self.quantity = quantity
		self.stock_limit = stock_limit
		self.save()

	def default_sale_guide(self):
		return self.sale_guides.first()

	def default_sale_guide_metric(self):
		default_sale_guide = self.default_sale_guide()
		if default_sale_guide:
			return default_sale_guide.metric

	def quantity_in_default_sale_guide_metric(self):
		default_sale_guide_metric = self.default_sale_guide_metric()
		purchase_metric = self.purchase_metric
		if default_sale_guide_metric and purchase_metric:
			return self.metric_system.convert(self.quantity, purchase_metric, default_sale_guide_metric)

	def stock_limit_in_default_sale_guide_metric(self):
		default_sale_guide_metric = self.default_sale_guide_metric()
		purchase_metric = self.purchase_metric
		if default_sale_guide_metric and purchase_metric:
			return self.metric_system.convert(self.stock_limit, purchase_metric, default_sale_guide_metric)


class Category(TimeStampedModel):
	name = models.CharField(max_length=128, unique=True)
	products = models.ManyToManyField(Product, through='ProductCategories', through_fields=('category', 'product'))

	def __str__(self):
		return self.name


class ProductCategories(TimeStampedModel):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Stock(TimeStampedModel):
	quantity = models.IntegerField()
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)


class SaleGuide(TimeStampedModel):
	metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
	price = models.IntegerField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_guides')

	def __str__(self):
		return f"{self.price} @ {self.metric}"


class OrderGroup(TimeStampedModel):
	reference = models.CharField(max_length=128)
	closed = models.BooleanField(default=False)
	customer = models.CharField(max_length=256, null=True)
	waiter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='waiter')
	cashier = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='cashier')
	status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)

	def __str__(self):
		return self.reference

	def total(self):
		return sum([(order.quantity*order.sale_price) for order in self.order_set.all()])


class Order(TimeStampedModel):
	reference = models.CharField(max_length=128)
	quantity = models.IntegerField()
	product_name = models.CharField(max_length=128)
	purchase_price = models.IntegerField()
	purchase_metric = models.CharField(max_length=128)
	sale_price = models.IntegerField()
	sale_metric = models.CharField(max_length=128)

	order_group = models.ForeignKey(OrderGroup, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	sale_guide = models.ForeignKey(SaleGuide, null=True, on_delete=models.SET_NULL)

	class Meta:
		permissions = [
			("can_make_orders", "Can make orders"),
			("can_mark_orders_as_ready", "Can mark orders as ready"),
			("can_mark_orders_as_served", "Can mark orders as served"),
		]

	def __str__(self):
		return self.reference



class Purchase(TimeStampedModel):
	quantity = models.IntegerField()
	product_name = models.CharField(max_length=128)
	purchase_price = models.IntegerField()
	purchase_metric = models.CharField(max_length=128)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	

class Profile(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    telephone = models.CharField(max_length=16, null=True)
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)

    def __str__(self):
    	return self.name

    def roles(self):
    	return ', '.join([group.name for group in self.user.groups.all()])


def get_user_profile(self):
	if getattr(self, "profile", None):
		return self.profile.name
	return self.username

User.add_to_class("__str__", get_user_profile)