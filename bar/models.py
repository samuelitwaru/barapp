from django.db import models
from django.contrib.auth.models import User
from .utils import STATUS_CHOICES, PENDING


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
	purchase_price = models.IntegerField(null=True)
	metric_system = models.ForeignKey(MetricSystem, null=True, on_delete=models.SET_NULL)
	purchase_metric = models.ForeignKey(Metric, null=True, on_delete=models.SET_NULL)
	categories = models.ManyToManyField('Category', through='ProductCategories', through_fields=('product', 'category'))


	def __str__(self):
		return self.name


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
	waiter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='waiter')
	cashier = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='cashier')

	def __str__(self):
		return self.reference


class Order(TimeStampedModel):
	reference = models.CharField(max_length=128)
	quantity = models.IntegerField()
	product_name = models.CharField(max_length=128)
	purchase_price = models.IntegerField()
	purchase_metric = models.CharField(max_length=128)
	sale_price = models.IntegerField()
	sale_metric = models.CharField(max_length=128)
	status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)

	order_group = models.ForeignKey(OrderGroup, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	sale_guide = models.ForeignKey(SaleGuide, null=True, on_delete=models.SET_NULL)
	# waiter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='waiter')
	# cashier = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='cashier')

	class Meta:
		permissions = [
			("can_make_orders", "Can make orders"),
			("can_mark_orders_as_ready", "Can mark orders as ready"),
			("can_mark_orders_as_served", "Can mark orders as served"),
		]

	def __str__(self):
		return self.reference




class Profile(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    telephone = models.CharField(max_length=16)
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)

    def __str__(self):
    	return self.name