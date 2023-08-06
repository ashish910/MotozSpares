from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        totalitem= 0
        BreakShoes = Product.objects.filter(category='B')
        Headlight = Product.objects.filter(category='HL')
        Engineoil = Product.objects.filter(category='E')
        Helmet = Product.objects.filter(category='H')
        chainlubeandcleaner = Product.objects.filter(category='CC')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'BreakShoes':BreakShoes,'Headlight':Headlight,'Engineoil':Engineoil,'Helmet':Helmet,'chainlubeandcleaner':chainlubeandcleaner,'totalitem':totalitem})



class ProductDetailView(View):
    def get(self, request, pk):
        totalitem= 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user 
        cart = Cart.objects.filter(user=user)
        amount =0.0
        shipping_amount = 30.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount +shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html',{'totalitem':totalitem})    

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 30.0
        cart_product =  [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 30.0
        cart_product =  [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)  

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 30.0
        cart_product =  [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


def breakshoe(request,data=None):
    if data == None:
        Breakshoes= Product.objects.filter(category='B')
    elif data == 'ASK' or data == 'NIKAVI':
        Breakshoes= Product.objects.filter(category='B').filter (brand=data)
    return render(request, 'app/breakshoe.html', {'Breakshoes':Breakshoes})

def headlight(request,data=None):
    if data == None:
        Headlight= Product.objects.filter(category='HL')
    elif data == 'UNOMINDA' or data == 'LUMAX':
        Headlight= Product.objects.filter(category='HL').filter (brand=data)
    return render(request,'app/headlight.html',{'Headlight':Headlight})

def engineoil(request,data=None):
    if data == None:
        Engineoil= Product.objects.filter(category='E')
    elif data == 'Castrol' or data == 'Motul'or data =='BAJAJ':
        Engineoil= Product.objects.filter(category='E').filter (brand=data)
    return render(request,'app/engineoil.html',{'Engineoil':Engineoil})

def helmet(request,data=None):
    if data == None:
        Helmet= Product.objects.filter(category='H')
    elif data == 'Studds' or data == 'Vega' or data =='Steelbird':
        Helmet= Product.objects.filter(category='H').filter (brand=data)
    return render(request,'app/helmet.html',{'Helmet':Helmet})    

def chainlube(request,data=None):
    if data == None:
        chainlubeandcleaner= Product.objects.filter(category='CC')
    elif data == 'Motul' or data == 'Waxpol' or data =='WD-40':
        chainlubeandcleaner= Product.objects.filter(category='CC').filter (brand=data)
    return render(request,'app/chainlube.html',{'chainlubeandcleaner':chainlubeandcleaner}) 


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})  
        
@login_required   
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 30.0
    totalamount = 0.0
    cart_product =  [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items} )

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")        

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})    
