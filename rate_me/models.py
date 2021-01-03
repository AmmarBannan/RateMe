from django.db import models
import re
import bcrypt
from datetime import date, datetime

class UserManager(models.Manager):
    def register_validator(self, user_info):
        errors = {}
        new_user = User.objects.filter(email = user_info['email'])
#names
        if (user_info['first_name'].isalpha()) == False: #user_info['first_name'] is from the form of registration
            if len(user_info['first_name']) <2 :
                errors["firstname"] = "First Name should be more than 2 characters." #["first_name"] is a key for errors dictionary can be any word
        if (user_info['last_name'].isalpha()) == False:
            if len(user_info['last_name']) <2 :
                errors["lastname"] = "Last Name should be more than 2 characters."
#email  
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(user_info['email']): #checking if email matches the regex           
            errors['email'] = "Invalid email address!"
        if len(new_user):
            errors['email'] = "email already exist"
#password
        if len(user_info['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if user_info['password'] != user_info['password_confirm']:
            errors['password_confirm']= "Password Dosent Match!"
        return errors
#birthday
        today = datetime.now().strftime("%Y%m%d")
        user_birthday = user_info['birthday'].replace("-", "")
        if len(user_info["birthday"]) > 0 and datetime.strptime(user_info["birthday"], '%Y-%m-%d') >= datetime.today() :
            errors["birthday"] = "Invalid Birth date"
        if (int(today[0:4]) - int(user_birthday[0:4])) <= 13:
            errors["birthday"] = "You should be at least 13 years old to register"

    def login_validator(self, user_info):
        errors = {}
        all_user = User.objects.filter(email = user_info['email'])
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match(user_info['email']):
        #     errors['email'] = "Wrong email address!"
        if not len(all_user):
            errors['email'] = "Email not registered! /Wrong Email"
        if len(user_info['password']) < 8:
            errors["password"] = "Password should be 8 characters minimum"
        if len(all_user) and not bcrypt.checkpw(user_info['password'].encode(), all_user[0].password.encode()):
            errors["password"] = "Wrong Password!"
        return errors
    
class CompaniesManager(models.Manager):
    def company_validator(self,company_info):
        errors = {}
#company's name
        new_company = Companies.objects.filter(name = company_info['name'])#chech if there is another company with the same name and gives error at the end
        if len(new_company):
            errors['name'] = "company name already exist"
            
        if (company_info['name'].isalpha()): 
            if len(company_info['name']) <2 :
                errors["name"] = "name's company should be more than 2 characters." 
#company's description
        if len(company_info['description']) <10 :
            errors["description"] = "name's company should be more than 10 characters." 
            
        return errors
        
    
class TypeManager(models.Manager):
    def type_validator(self,type_info):
        errors = {}
        new_type = Car_type.objects.filter(name = type_info['name'])
#type's name
        if (type_info['name'].isalpha()) : 
            if len(type_info['name']) <2 :
                errors["name"] = "type name to short should be more than 2 characters." 
        if len(new_type):
            errors['name'] = "this type is already exist"
            
        
        return errors

        

class user_roles(models.Model):
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=90) 
    birthday = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(user_roles, related_name="users", on_delete = models.CASCADE,default=2)
    objects = UserManager()
    
class Companies(models.Model):
    name =  models.CharField(max_length=255)
    description = models.TextField(max_length=1200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ForeignKey(User, related_name="companies", on_delete = models.CASCADE)
    objects = CompaniesManager()
    
class Car_type(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Companies, related_name="type", on_delete = models.CASCADE)
    nor = models.IntegerField(default=0)
    avg = models.DecimalField(decimal_places=2, max_digits=4,default=1.0)
    objects = TypeManager()
    
class Rating(models.Model):
    comfort = models.IntegerField(null=True)
    durable = models.IntegerField(null=True)
    safety = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    fuel = models.IntegerField(null=True)
    avg = models.DecimalField(decimal_places=2, max_digits=4,default=1.0,null=True)
    comment = models.TextField(max_length=255 ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="rate", on_delete = models.CASCADE)
    car_type = models.ForeignKey(Car_type, related_name="rate", on_delete = models.CASCADE)

def add_new_user(newUser):
    user = User.objects.filter(email = newUser['email'])
    if len(user) == 0:
        if newUser['password_confirm'] == newUser['password']:
            password = newUser['password']  #hashing user password
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
            User.objects.create(first_name=newUser['first_name'],last_name=newUser['last_name'],email=newUser['email'],password=hashed, birthday=newUser['birthday'], gender=newUser['gender'])  #newUser['key name from form']
            new_user_info = User.objects.last() 
            return new_user_info
    return False

def user_login(login_info):
    user_exist = User.objects.filter(email=login_info['email'])
    if len(user_exist):
        password= login_info['password']
        if bcrypt.checkpw(password.encode(), user_exist[0].password.encode()):
            return user_exist[0]
    return False