from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  , login , logout
from django.contrib import messages

def Login(request):
    if request.method =="POST":
        Data = request.POST
        username=Data.get('Name')
        Password =Data.get('Password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid UserName")
            return redirect('/')
        user = authenticate(username=username,password=Password)
        if user is None:
            messages.error(request ," Wrong PassWord ❌")
            return redirect('/')
        else:
            login(request , user)    
            return redirect('/home/' ,{"user":user})
    return render(request,"expenses/login_page.html",{'Page':'Login'})

def register_user(request):
    if request.method =="POST":
        Data = request.POST
        username =Data.get('username')
        first_name=Data.get('first_name')
        last_name=Data.get('last_name')
        email= Data.get('email')
        Password =Data.get('password')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request ,"UserName Already Taken -- 👺 -- UserName Already Exists !")
            return redirect("/register/")
        user = User.objects.create(username=username ,first_name=first_name,last_name=last_name ,email=email)
        user.set_password(Password)
        user.save()
        messages.info(request ,"Account Create Successfully 🎉")
        login(request,user)
        return redirect('/home/' ,{"user":user})
    return render(request,"expenses/Register.html",{'Page':'Register_At_Expense'})

def logout_page(request):
    logout(request)
    return redirect('/')

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
        # for searching Category
    if request.GET.get('search'):    # print(request.GET.get('search'))
        expenses = expenses.filter(category__icontains = request.GET.get('search'))
    context ={'expenses':expenses}
    return render(request, "expenses/view_expenses.html", context)

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
