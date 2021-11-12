from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from ..models import MetricSystem
from ..forms import CreateMetricSystemForm


class MetricSystemsPageView(TemplateView):
	template_name = "metric-system/metric-systems.html"

	def get_context_data(self, ** kwargs):
		context = super().get_context_data(**kwargs)
		create_metric_system_form = CreateMetricSystemForm()
		context['metric_systems'] = MetricSystem.objects.all()
		context["create_metric_system_form"] = create_metric_system_form
		return context

@login_required
def create_metric_system(request):
	create_metric_system_form = CreateMetricSystemForm(request.POST)
	if create_metric_system_form.is_valid():
		data = create_metric_system_form.cleaned_data
		metric_system = MetricSystem(name=data["name"])
		metric_system.save()
		messages.success(request, "Metric system created.")
		return redirect("bar:get_metric_systems")

