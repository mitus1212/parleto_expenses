import datetime
from django.urls import reverse
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

    def expenses_amount(self):
        return self.expense_set.filter(category=self.id).count()
    
    def expenses_sum(self):
        category_sum = 0
        category_expenses = Expense.objects.filter(category=self.id)
        for category in category_expenses:
            category_sum += category.amount
        return category_sum  

    def get_absolute_url(self):
        return reverse("expenses:category-detail",kwargs={'pk':self.pk})

class Expense(models.Model):
    class Meta:
        ordering = ('-date', '-pk')
    category = models.ForeignKey(Category, models.PROTECT, null=True, blank=True)

    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    date = models.DateField(default=datetime.date.today, db_index=True)

    def __str__(self):
        return f'{self.date} {self.name} {self.amount}'
