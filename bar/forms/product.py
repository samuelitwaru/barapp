from django import forms
from django.forms import ModelForm
from ..models import Product, Category


class CreateProductForm(ModelForm):
	class Meta:
		model = Product
		fields = "__all__"
		exclude = ("quantity", "categories", "purchase_metric", "purchase_price")

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

	def __init__(self, categories=None, product=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
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