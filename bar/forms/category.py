from django import forms
from django.forms import ModelForm
from ..models import Category


class CreateCategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = "__all__"
		exclude = ("products",)


class UpdateCategoryForm(CreateCategoryForm):
	
	def __init__(self, category, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.category = category

	def clean(self):
		name = self.data.get("name")
		print(">>>>>fdoingn", Category.objects.exclude(id=self.category.id).filter(name=name).count())
		if Category.objects.exclude(id=self.category.id).filter(name=name).count():
			self.add_error('name', "Product with this barcode already exists")


class DeleteCategoryForm(forms.Form):
	pass