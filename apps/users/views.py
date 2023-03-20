from django.shortcuts import render , redirect
from apps.users.models import User,Followers
from django.contrib.auth import authenticate , login
from django.http.response import HttpResponse
from django.db.models import Q
# Create your views here.
def register(request):
    if request.method == 'POST':
        full_name=request.POST.get('full_name')
        email_phone_number=request.POST.get('email_phone_number')
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password == confirm_password:
            try:
                try:
                    user=User.objects.create(full_name=full_name,email=email_phone_number,username=username)
                except:
                    user=User.objects.create(full_name=full_name,phone_number=email_phone_number,username=username)
                user.set_password(password)
                user.save()
                user=User.objects.get(username=username)
                user=authenticate(username=username,password=password)
                login(request , user)
                return redirect('index')
            except:
                return redirect('register')
    return render(request , 'register.html')

def user_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('index')
        except:
            return HttpResponse('<h1>Вы не правильно вели пароль или имя пользователь </h1>')
    return render(request, 'sign-in.html')

def profile(request,username):
    user = User.objects.get(username = username)
    follow_status = Followers.objects.filter(from_user = request.user , to_user = user)
    if 'follow' in request.POST:
        try:    
            follow = Followers.objects.get(to_user=user , from_user = request.user)
            follow.delete()
            return redirect('account' ,user.username)
        except:
            follow = Followers.objects.create(to_user = user , from_user = request.user)
            follow.save()
            return redirect('account' , user.username)
    context= {
        'user':user,
        'follow_status':follow_status
    }
    return render(request,'my_account.html',context)


def account_settings(request,username):
    user = User.objects.get(username = username)
    if request.user != user:
        return redirect('index')
    if request.method == 'POST':
        gender = request.POST.get('gender')
        relationship = request.POST.get('relationship')
        number = request.POST.get('number')
        occupation = request.POST.get('occupation')
        description = request.POST.get('description')
        full_name = request.POST.get('full_name')
        profile_image = request.FILES.get('profile_image')
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user.gender = gender
            user.number =number
            user.relationship = relationship
            user.occupation = occupation
            user.description = description
            user.full_name = full_name
            user.profile_image = profile_image
            user.email = email
            user.username = username
            user.save()
        except:
            return redirect('account')
        
    context = {
        'user':user,
    }
    return render(request , 'account_settings.html' , context)

def followers(request, id):
    user = User.objects.get(id = id)
    user_followers = Followers.objects.filter(to_user = user)
    if request.method == "POST":
        if 'delete' in request.POST:
            follower = request.POST.get('follower')
            follow_status = Followers.objects.get(id = int(follower))
            follow_status.delete()
            return redirect('followers', user.id)
    context = {
        'user':user,
        'user_followers':user_followers
    }
    return render(request, 'followers.html', context)


            
def follows(request, id):
    user = User.objects.get(id = id)
    follow_status = Followers.objects.filter(from_user = user)
    if 'follow' in request.POST:
        floow = request.POST.get('follow')
        
        try:    
            follow = Followers.objects.get(to_user_id=floow , from_user = request.user)
            follow.delete()
            return redirect('account' ,user.username)
        except:
            return redirect('follows' ,user.id)
    context = {
        'user':user,
        'follow_status':follow_status
    }
    return render(request, 'follows.html', context)
    
