from django import forms
from django.forms import ModelForm
from ..models import Product, Category, MetricSystem


class CreateProductForm(ModelForm):
	class Meta:
		model = Product
		fields = "__all__"
		exclude = ("quantity", "stock_limit", "categories", "purchase_metric", "purchase_price")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["barcode"].required = False
		self.fields["description"].required = False


class UpdateProductForm(CreateProductForm):

	def __init__(self, product, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.product = product

	def clean(self):
		barcode = self.data.get("barcode")
		if Product.objects.exclude(id=self.product.id).exclude(barcode=None).filter(barcode=barcode).count():
			self.add_error('barcode', "Product with this barcode already exists")



class UpdateProductCategoriesForm(forms.Form):

	def __init__(self, categories=[], product=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.category_count = len(categories)
		if categories and product:
			self.categories = categories
			self.product = product
			self.product_categories = self.product.categories.all()
			for category in categories:
				self.fields[f"cat_{category.id}"] = forms.BooleanField(label=f"{category.name}", required=False, initial=(category in self.product_categories))

	def clean(self):
		try:
			cat_ids = list(map(lambda item: int(item.split('_')[1]), list(filter(lambda item: item.startswith('cat'), self.data.keys()))))
			self.cleaned_data["categories"] = Category.objects.filter(id__in=cat_ids)
		except Exception as e:
			print(e)
			raise forms.ValidationError(f"Failed to compute categories with error: {e}")


class UpdateProductPurchasingForm(ModelForm):
	class Meta:
		model = Product
		fields = ("purchase_metric", "purchase_price")

	def __init__(self, product, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["purchase_metric"].widget.choices = [(metric.id, str(metric)) for metric in product.metric_system.metric_set.all()]


class AddProductStockForm(UpdateProductPurchasingForm):
	quantity = forms.IntegerField(label="Quantity")

	def __init__(self, product, *args, **kwargs):
		super().__init__(product=product, *args, **kwargs)
		self.product = product

	def clean(self):
		cleaned_data = super().clean()
		quantity = cleaned_data["quantity"]
		purchase_metric = cleaned_data.get("purchase_metric")
		if quantity < 1:
			self.add_error('quantity', "Value cannot be less than 1")



class FilterProductsForm(forms.Form):
	metric_system = forms.IntegerField(label="Metric system", required=False,  widget=forms.Select(choices=[(0, 'ANY')]))
	category = forms.IntegerField(label="Category", required=False,  widget=forms.Select(choices=[(0, 'ANY')]))

	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["metric_system"].widget.choices += [(metric_system.id, metric_system.name) for metric_system in MetricSystem.objects.all()]
		self.fields["category"].widget.choices += [(category.id, category.name) for category in Category.objects.all()]

