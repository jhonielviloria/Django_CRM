import django_filters as df
from django import forms
from .models import *


class OrderFilter(df.FilterSet):
	start_date = df.DateFilter(field_name="created", lookup_expr="gte", label="Start Date")
	end_date = df.DateFilter(field_name="created", lookup_expr="lte", label="End Date")
	class Meta:
		model = Order
		fields = '__all__'
		exclude = ['customer', 'created', 'updated']
