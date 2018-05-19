from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .forms import UserForm
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

def index(request):
    if 'user' in request.session:
        return redirect(reverse('dash:dashboard'))
    return render(request, 'dashboard/index.html')

def signin(request):
    if 'user' in request.session:
        return redirect(reverse('dash:dashboard'))

    if request.method == "GET":
        return render(request, 'dashboard/signin.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('pw') 
        
        user = User.objects.filter(email = email).first()
        
    if user:
        valid_pw = bcrypt.checkpw(password.encode(), user.password.encode())
        if valid_pw:
            request.session['user'] = { 'id' : user.id, 'admin' : User.ADMIN == user.level }
            return redirect(reverse('dash:dashboard'))
        else:
            messages.error(request, 'Invalid user/password')
            return redirect(reverse('dash:signin'))                            
    else:
        messages.error(request, 'User does not exist')
        return redirect(reverse('dash:signin'))                                
    
def register(request):
    if 'user' in request.session:
        return redirect(reverse('dash:dashboard'))

    if request.method == 'GET':
        return render(request, 'dashboard/register.html', { 'form' : UserForm() })
    else:        
        form = UserForm(request.POST)
        errors = User.objects.validate(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('dash:register'))
        else:
            user = form.save(commit=False)
            user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            if User.objects.count() == 0:
                user.level = User.ADMIN
            user.save()
            request.session['user'] = { 'id' : user.id, 'admin' : User.ADMIN == user.level }
            return redirect(reverse('dash:dashboard')) 
    
def dashboard(request):
    if not 'user' in request.session:
        return redirect(reverse('dash:signin'))
    return render(request, 'dashboard/dashboard.html', { 'users' : User.objects.all() })

    
def profile(request):
    if not 'user' in request.session:
        return redirect(reverse('dash:signin'))
    if request.method == 'GET':        
        user = User.objects.get(id=request.session.get('user')['id'])
        return render(request, 'dashboard/profile.html', { 'form' : UserForm(instance=user) })           
    else:
        form = UserForm(request.POST)
        errors = User.objects.validate(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error)
            return redirect(reverse('dash:create'))
        else:
            user = form.save(commit=False)
            user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            user.save()
            return redirect(reverse('dash:dashboard'))
                

    
def new(request):
    if not request.session['user']:
        return redirect(reverse('dash:dashboard')) 
    elif not request.session['user']['admin']:
        return redirect(reverse('dash:dashboard'))
    else:
        if request.method == 'GET':
            return render(request, 'dashboard/new.html', { 'form' : UserForm() })
        else:
            form = UserForm(request.POST)
            errors = User.objects.validate(request.POST)
            if errors:
                for tag, error in errors.iteritems():
                    messages.error(request, error)
                return redirect(reverse('dash:create'))
            else:
                user = form.save(commit=False)
                user.password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
                user.save()
                return redirect(reverse('dash:dashboard'))                        

    
def show(request, id):
    return HttpResponse('show {}'.format(id))
    
def edit(request, id):
    return HttpResponse('edit {}'.format(id))

def logout(request):
    request.session.clear()
    return redirect(reverse('dash:index'))   
    
def destroy(request):
    if not request.session['user']:
        return redirect(reverse('dash:dashboard')) 
    elif not request.session['user']['admin']:
        return redirect(reverse('dash:dashboard'))
    else:
        print request.POST.get('id')
        id = int(request.POST.get('id'))
        User.objects.get(id=id).delete()
        return redirect(reverse('dash:dashboard'))
        
           
