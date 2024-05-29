from django.http import HttpResponse
from django.shortcuts import render, redirect
# from .models import session, User
from .models import  UserModel,Phone_number,Parent_details,engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,or_,and_,not_
from django import forms
from django.contrib import messages
from django.http import JsonResponse

Session = sessionmaker(bind=engine)
session =Session()

def login_view(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        check_user = session.query(UserModel).where(and_(UserModel.password ==password,UserModel.name ==username)).all()
        if check_user:
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
     else:
        return render(request, 'login.html')



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email') 
        roles = request.POST.get('roles') 
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        phone_number = request.POST.get('phone_number') 
        exist_user = session.query(UserModel).where(or_(UserModel.password ==password,UserModel.name ==username)).all()
        for user in exist_user:
            print(user.name,"email",user.email)
        else:
            new_user = UserModel(name=username,password=password, email=email,roles=roles)
            new_phone = Phone_number(phone_number =phone_number,user=new_user)
            parents=Parent_details(Mother_Name=mother_name,Father_Name=father_name)
            new_user.parents.append(parents)
            session.add(new_user)
            session.add(new_phone)
            session.commit()
            return redirect('login')
    else: 
        return render(request, 'register.html')

def list_users(request):
    # Querying all users
    users = session.query(UserModel).all()
    user_list = '<br> '.join([f"{user.name}  email:{user.email}" for user in users])
    return HttpResponse(f"Users in the database:<br><br> {user_list} ")

def dashboard(request):
    users = session.query(UserModel).all()
    return render(request, 'dashboard.html', {'users': users})

def delete_user(request, user_id):
    user = session.query(UserModel).filter_by(id =user_id).first()
    if user:
            # Delete the user object
            session.delete(user)
            session.commit()
            return redirect('dashboard')
    else:
        print("User not found")

def edit_user(request, user_id):
    try:
        user = session.query(UserModel).filter(UserModel.id == user_id).first()
        if user:
            user.name = request.POST.get('new_name')
            user.password = request.POST.get('new_password')
            phone = Phone_number(phone_number =request.POST.get('new_phone_number'),user=user)
            session.add(phone)
            session.add(user)
            session.commit()
        else:
            print("User not found")
    except Exception as e:
        session.rollback()
    return redirect('dashboard')

def filter_users(request):
    name = request.GET.get('name')
    filters = session.query(UserModel).filter_by(name =name).all()
    users_data = [{'name': user.name, 'email': user.email} for user in filters]
    return JsonResponse(users_data, safe=False)