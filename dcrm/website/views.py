from django.shortcuts import render, redirect #what is the purpuse of redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SingUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
    
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        #authenticate
        user = authenticate(request, username=username, password=password) #authenticate function is check user credentials
        if user is not None: #This line checks if the user object is not None, meaning the authentication was successful.
            login(request, user) #why did we used here login method
            messages.success(request, "You Have Been Logged In!")
            return redirect ('home')
        
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect ('home')
    
    else: 
        return render (request, 'home.html', {'records' : records})




def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect ('home')





def regiter_user(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome! ")
            return redirect('home')
        
    else:
        form = SingUpForm()
            
    return render (request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')
    
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        
        messages.success(request, "Record Deleted Successfully...")
        return redirect ('home')
    
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect ('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Addedd...")
                return redirect('home')
    
        return render(request, 'add_record.html', {'form':form})
    
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
    
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')