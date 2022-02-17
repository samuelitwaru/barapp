from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from ..models import MetricSystem
from ..forms import CreateMetricSystemForm
from ..decorators import *
from django.utils.decorators import method_decorator



class MetricSystemsPageView(TemplateView):
	template_name = "metric-system/metric-systems.html"

	def get_context_data(self, ** kwargs):
		context = super().get_context_data(**kwargs)
		create_metric_system_form = CreateMetricSystemForm()
		context['metric_systems'] = MetricSystem.objects.all()
		context["create_metric_system_form"] = create_metric_system_form
		return context
	
	@method_decorator(groups_required("Admin", "Cashier"))
	def get(self, request, *args, **kwargs):
		metric_systems = MetricSystem.objects.all()
		create_metric_system_form = CreateMetricSystemForm()
		context = {
			'metric_systems': metric_systems,
			'create_metric_system_form': create_metric_system_form,
		}
		return render(request, "metric-system/metric-systems.html", context)


@groups_required("Admin", "Cashier")
@login_required
def create_metric_system(request):
	create_metric_system_form = CreateMetricSystemForm(request.POST)
	if create_metric_system_form.is_valid():
		data = create_metric_system_form.cleaned_data
		metric_system = MetricSystem(name=data["name"])
		metric_system.save()
		messages.success(request, "Metric system created.")
		return redirect("bar:get_metric_systems")



@groups_required("Admin", "Cashier")
@login_required
def delete_metric_system(request, id):
	metric_system = MetricSystem.objects.get(id=id)
	metric_system.delete()
	messages.success(request, "Metric System deleted")
	return redirect('bar:get_metric_systems')

