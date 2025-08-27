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
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    if request.method == "POST":
        title = request.POST['title']
        amount = request.POST['amount']
        category = request.POST['category']
        date_val = request.POST['date']
        notes = request.POST.get('notes', '')

        Expense.objects.create(
            user=request.user,  
            title=title,
            amount=amount,
            category=category,
            date=date_val,
            notes=notes
        )
        return redirect('view_expenses')

    filter_by = request.GET.get('filter_by')
    query = request.GET.get('query', '').strip()

    if filter_by and query:
        try:
            if filter_by == "category":
                expenses = expenses.filter(category__icontains=query)
            elif filter_by == "title":
                expenses = expenses.filter(title__icontains=query)
            elif filter_by == "amount":
                if query.replace('.', '', 1).isdigit():
                    expenses = expenses.filter(amount=query)
                else:
                    messages.error(request, "Please enter a valid number for amount.")
            elif filter_by == "year":
                if query.isdigit():
                    expenses = expenses.filter(date__year=int(query))
                else:
                    messages.error(request, " Year must be a number (e.g., 2025).")
            elif filter_by == "month":
                if query.isdigit():
                    expenses = expenses.filter(date__month=int(query))
                else:
                    messages.error(request, " Month must be between 1-12.")
            elif filter_by == "day":
                if query.isdigit():
                    expenses = expenses.filter(date__day=int(query))
                else:
                    messages.error(request, " Day must be between 1-31.")
        except Exception:
            messages.error(request, "Invalid search input.")

    return render(request, "expenses/view_expenses.html", {"expenses": expenses})
# UPDATE
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user) 
    if request.method == "POST":
        expense.title = request.POST['title']
        expense.amount = request.POST['amount']
        expense.category = request.POST['category']
        expense.date = request.POST['date']
        expense.notes = request.POST.get('notes', '')
        expense.save()
        return redirect('view_expenses')
    return render(request, "expenses/edit_expenses.html", {"expense": expense})

#delete
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id,user=request.user)
    expense.delete()
    return redirect('view_expenses')


#dashboard
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    filter_by = request.GET.get('filter_by')
    query = request.GET.get('query', '').strip()

    if filter_by and query:
        try:
            if filter_by == "category":
                expenses = expenses.filter(category__icontains=query)
            elif filter_by == "amount":
                if query.replace('.', '', 1).isdigit():
                    expenses = expenses.filter(amount=query)
                else:
                    messages.error(request, "Please enter a valid number for amount.")
            elif filter_by == "year":
                if query.isdigit():
                    expenses = expenses.filter(date__year=int(query))
                else:
                    messages.error(request, " Year must be a number (e.g., 2025).")
            elif filter_by == "month":
                if query.isdigit():
                    expenses = expenses.filter(date__month=int(query))
                else:
                    messages.error(request, " Month must be between 1-12.")
            elif filter_by == "day":
                if query.isdigit():
                    expenses = expenses.filter(date__day=int(query))
                else:
                    messages.error(request, " Day must be between 1-31.")
        except Exception:
            messages.error(request, "Invalid search input.")

    total = sum(exp.amount for exp in expenses)
    return render(request, "expenses/dashboard.html", {"total": total, "expenses": expenses})
