from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense

# CREATE & READ
def view_expenses(request):
    expenses = Expense.objects.all().order_by('-date')
    if request.method == "POST":
        title = request.POST['title']
        amount = request.POST['amount']
        category = request.POST['category']
        date_val = request.POST['date']
        notes = request.POST.get('notes', '')
        Expense.objects.create(title=title, amount=amount, category=category, date=date_val, notes=notes)
        return redirect('view_expenses')
    return render(request, "expenses/view_expenses.html", {"expenses": expenses})

# UPDATE
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == "POST":
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.notes = request.POST.get('notes', '')
        expense.save()
        return redirect('view_expenses')
    return render(request, "expenses/edit_expenses.html", {"expense": expense})

# DELETE
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('view_expenses')

# DASHBOARD
def dashboard(request):
    expenses = Expense.objects.all()
    total = sum(exp.amount for exp in expenses)
    return render(request, "expenses/dashboard.html", {"total": total, "expenses": expenses})
