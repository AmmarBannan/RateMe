from django.shortcuts import render, redirect,HttpResponse
from .models import User
from . import models
from json import dumps
from django.http import JsonResponse
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from decimal import Decimal


# Create your views here.
def drift(request):
    return redirect('/rate_me/home')

def register(request):
    if request.method == 'POST':
        errors = models.User.objects.register_validator(request.POST) #check if there are errors in error dictionary and redirect to same page to fill form again 
        if len(errors)>0:  #if errors exist loop over the dictionary and show the messages
            for key, value in errors.items():
                messages.error(request, value) #show the messages value
            return redirect('/rate_me/registration')                                                                   
        else: #if there are no errors >> create new user
            user = models.add_new_user(request.POST)
            if user is not None:
                if 'id' not in request.session:
                    request.session['id'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
            return redirect('/rate_me/home')
    return redirect('/')

def log_in(request):
    return render(request,'login.html')

def registration(request):
    return render(request,'Registration.html')

def login(request):
    if request.method=='POST':
        errors = models.User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/rate_me/log_in')
        else:
            user = models.user_login(request.POST)
            if user is not None:
                if 'id' not in request.session:
                    request.session['id'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                return redirect('/rate_me/home')
    return redirect('/rate_me/log_in')

def home(request):
    # if 'id' in request.session:
    #     context={
    #         'companies':models.Companies.objects.all(),
    #     }
    if 'id' in request.session:
        user=User.objects.get(id=request.session['id'])
        context = {
            'user':user,
            'companies':models.Companies.objects.all(),
            'type_list':models.Car_type.objects.all(),
            'rate':models.Rating.objects.all(),
        }
    else :
        context = {
            'companies':models.Companies.objects.all(),
            'type_list':models.Car_type.objects.all(),
            'rate':models.Rating.objects.all(),
            }
    if 'term' in request.GET:
        qs = models.Companies.objects.filter(name__istartswith=request.GET.get('term'))
        names = list()
        for type in qs:
            names.append(type.name)
        return JsonResponse(names, safe=False)
    return render(request,'test.html',context)

def logout(request):
    if 'id' in request.session:
        del request.session['id']   
    return redirect('/')

def category(request,id):
    one_comp=models.Companies.objects.get(id=id)
    if 'id' in request.session:
        user=models.User.objects.get(id=request.session['id'])
        context={
            'user':user,
            'companies':one_comp,
            'types':one_comp.type.all(),
        }
    else:
        context={
            'companies':one_comp,
            'types':one_comp.type.all(),
        }
    return render(request,'Categories.html',context)

def item(request,id):
    one_type=models.Car_type.objects.get(id=id)
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        rate=models.Rating.objects.filter(car_type=one_type),

        context={
            'Comfort':4,
            'user':user,
            'id_item':id,
            'type':one_type,
            'user_review':models.Rating.objects.filter(car_type=one_type,user=user),
            'other_review':models.Rating.objects.filter(car_type=one_type).exclude(user=user),
        }
    else:
        context={
            'id_item':id,
            'type':one_type,
            'rates':models.Rating.objects.all(),
        }
    return render(request,'item.html',context)

def rate(request,item_id):
    if 'POST' in request.method:
        print("%^"*15,request.POST['Comfort'])
        if 'id' in request.session:
            use=User.objects.get(id=request.session['id'])
            item=models.Car_type.objects.get(id=item_id)
            com=int(request.POST['Comfort'])
            dur=int(request.POST['Durable'])
            saf=int(request.POST['Safety'])
            pri=int(request.POST['Price'])
            fu=int(request.POST['Fuel'])
            avg=float(com+dur+saf+pri+fu)/5
            comm=request.POST['comment']
            summ=Decimal(item.avg*item.nor)
            if models.Rating.objects.filter(user=use,car_type=item):
                x=models.Rating.objects.get(user=use,car_type=item)
                x.comfort=com
                x.safety=saf
                x.durable=dur
                x.fuel=fu
                x.price=pri
                x.avg=avg
                x.comment=comm
                x.save()
            else:
                models.Rating.objects.create(comfort=com,durable=dur,safety=saf,price=pri,fuel=fu,avg=avg,comment=comm,user=use,car_type=item)
                item.nor+=1
                item.save()
            summ+=Decimal(avg)
            item.avg=summ/item.nor
            item.save()
    return redirect('/rate_me/type/'+str(item_id))

def deleteit(request,id_item,id_review):
    review=models.Rating.objects.get(id=id_review)
    item=models.Car_type.objects.get(id=id_item)
    if item.nor < 2:
        item.nor=2
    item.nor-=1
    item.save()
    review.delete()
    summ=Decimal(item.avg*item.nor-review.avg)
    item.avg=summ/item.nor
    item.save()
    return redirect('/rate_me/type/'+str(id_item))

def check(request,id):
    if 'id' in request.session:
        user=User.objects.get(id=id)
        admin=models.user_roles.objects.get(id=1)
        if user.admin == admin:
            return redirect('/admin/'+str(id))
        else:
            return redirect('/user/'+str(id))

def admin(request,id):
    if 'id' in request.session:
        id=request.session['id']
        context={
            'user':User.objects.get(id=id),
            'users':User.objects.exclude(id=id),
            'companies':models.Companies.objects.all(),
            'rates':models.Rating.objects.all(),
            'types':models.Car_type.objects.all(),
        }
        return render(request,'admin_main.html',context)
    return redirect('/')

def user(request,id):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        context = {
            'user': user,
            'companies': models.Companies.objects.all(),
            'type_list': models.Car_type.objects.all(),
            'rates': models.Rating.objects.filter(user=user),
            'Comfort':3,
            # 'Safety':3,
        }
    return render(request, 'user.html', context)

def makeadmin(request,id1):
    if 'id' in request.session:
        id=request.session['id']
        users=User.objects.all()
        admin=models.user_roles.objects.get(id=1)
        for user in users:
            if  user.id == id1:
                user.admin=admin
    return redirect('/admin/'+str(id))

def deleteuser(request,id1):
    id=request.session('id')
    use=User.objects.get(id=id1)
    use.delete()
    return redirect('/user'+str(id))

def upload(request):
    if 'id' in request.session:
        if 'POST' == request.method:
            id=request.session['id']
            use=User.objects.get(id=id)
            company=models.Companies.objects.filter(name=request.POST['name'])
            if company:
                return HttpResponse('company already exists')
            else:
                models.Companies.objects.create(name=request.POST['name'],description=request.POST['description'],users=use)
                return redirect('admin/'+str(id))

def update(request,id):
    if 'id' in request.session:
        user=User.objects.get(id=id)
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']  
        user.save()
    return redirect('/')

def deletetype(request,id):
    if 'id' in request.session:
        if 'POST' == request.method:
            id=request.session['id']
            x=models.Car_type.objects.get(id=id)
            x.delete()
            return redirect('admin/'+str(id))   

def uploadtype(request,id):
    if 'id' in request.session:
        if 'POST' == request.method:
            use=User.objects.get(id=request.session['id'])
            company=models.Companies.objects.get(id=request.POST['company'])
            ctype=models.Car_type.objects.filter(name=request.POST['name'])
            if ctype:
                return HttpResponse('company already exists')
            else:
                models.Car_type.objects.create(name=request.POST['name'],description=request.POST['description'],company=company)
                return redirect('/admin/'+str(id))

def search(request):
    return redirect('/rate_me/company/1')