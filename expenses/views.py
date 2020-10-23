from django.views.generic.list import ListView

from .forms import ExpenseSearchForm, CategoryForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            category = form.cleaned_data['category']
            if category:
                queryset = queryset.filter(category=category)

            grouping = form.cleaned_data['grouping']
            if grouping:
                queryset = queryset.order_by('date', '-pk')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            **kwargs)


class CategoryListView(ListView):
    login_url = '/category/'

    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        
        return super().get_context_data(
            object_list=queryset,
            **kwargs)


class CreateCategoryView(CreateView):
    redirect_field_name = 'expenses/expense_list.html'

    form_class = CategoryForm

    model = Category

class CategoryDetailView(DetailView):
    model = Category