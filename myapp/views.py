import email
from itertools import product
from time import timezone
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Transaction
from myapp.templates.paytm import generate_checksum, verify_checksum
from . models import Contact, Product,User,Wishlist,Cart,Order
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
    try:
        user=User.objects.get(email=request.session['email'])
        products=Product.objects.all()
        if user.usertype=='user':
            return render(request,'index.html',{'products':products})
        else:
            return render(request,'seller_index.html')
    except:
        products=Product.objects.all()
        return render(request,'index.html',{'products':products})

def seller_index(request):
    return render(request,'seller_index.html')

def about(request):
    return render(request,'about.html')


def validate_signup(request):
    email=request.GET.get('email')
    data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
    return JsonResponse(data)


def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    try:
        amount = int(request.POST['amount'])

    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    
    cart=Cart.objects.filter(user=user)
    for i in cart:
        i.payment_status="paid"
        i.date=timezone.now()
        i.save()
    cart=Cart.objects.filter(user=user,payment_status="pending")
    request.session['cart_count']=len(cart)
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)

    Order.objects.create(
        fname=request.POST['fname'],
        lname=request.POST['lname'],
        state=request.POST['state'],
        street_address1=request.POST['street_address1'],
        street_address2=request.POST['street_address2'],
        city=request.POST['city'],
        postcode=request.POST['postcode'],
        mobile=request.POST['mobile'],
        email=request.POST['email']
    )
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)



def shop(request):
    products=Product.objects.all()
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})

def category_men(request):
    products=Product.objects.filter(product_category="men")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})
    

def category_women(request):
    products=Product.objects.filter(product_category="women")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})



def category_kids(request):
    products=Product.objects.filter(product_category="kids")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})

def color_red(request):
    products=Product.objects.filter(product_color="red")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})
    

def color_green(request):
    products=Product.objects.filter(product_color="green")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})



def color_blue(request):
    products=Product.objects.filter(product_color="blue")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})

def color_white(request):
    products=Product.objects.filter(product_color="white")
    men=len(Product.objects.filter(product_category="men"))
    women=len(Product.objects.filter(product_category="women"))
    kids=len(Product.objects.filter(product_category="kids"))
    red=len(Product.objects.filter(product_color="red"))
    green=len(Product.objects.filter(product_color="green"))
    blue=len(Product.objects.filter(product_color="blue"))
    white=len(Product.objects.filter(product_color="white"))
    return render(request,'shop.html',{'products':products,'men':men,'women':women,'kids':kids,'red':red,'green':green,'blue':blue,'white':white})



    



def cart(request):
    return render(request,'cart.html')

def shop_single(request):
    return render(request,'shop-single.html')

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        msg="Contact Saved Successfully"
        return render(request,'contact.html',{'msg':msg})
    else:
        return render(request,'contact.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    usertype=request.POST['usertype']
                )
                msg="Signed Up Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password And Confirm Password Does Not Macthed"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                if user.usertype=='user':
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    wishlist=Wishlist.objects.filter(user=user)
                    request.session['wishlist_count']=len(wishlist)
                    cart=Cart.objects.filter(user=user,payment_status='pending')
                    request.session['cart_count']=len(cart)
                    msg="Logged In Successfully"
                    return redirect('index')
                else:
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    msg="Logged In Successfully"
                    return render(request,'seller_index.html',{'msg':msg})
            else:
                msg="Email or Password Incorrect"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Registered"
            return render(request,'login.html',{'msg':msg})        
    else:
        return render(request,'login.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request,'login.html')
    except:
        return render(request,'login.html')

def change_password(request):
    if request.method=='POST':
        user=User.objects.get(email=request.session['email'])
        if request.POST['old_password']==user.password:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                msg="Password Changed Successfully"
                return render(request,'login.html',{'msg':msg})

            else:
                msg="Password And Confirm Password Does Not Matched"
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')


def seller_change_password(request):
    if request.method=='POST':
        user=User.objects.get(email=request.session['email'])
        if request.POST['old_password']==user.password:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                msg="Password Changed Successfully"
                return render(request,'seller_change_password.html',{'msg':msg})

            else:
                msg="Password And Confirm Password Does Not Matched"
                return render(request,'seller_change_password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            return render(request,'seller_change_password.html',{'msg':msg})
    else:
        return render(request,'seller_change_password.html')

def seller_add_product(request):
    if request.method=="POST":
        product_seller=User.objects.get(email=request.session['email'])
        Product.objects.create(
            product_seller=product_seller,
            product_name=request.POST['product_name'],
            product_category=request.POST['product_category'],
            product_size=request.POST['product_size'],
            product_color=request.POST['product_color'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image']
        )

        msg="Product Added Successfully"
        return render(request,'seller_add_product.html',{'msg':msg})
    else:
        return render(request,'seller_add_product.html')



def seller_view_product(request):
        product_seller=User.objects.get(email=request.session['email'])
        products=Product.objects.filter(product_seller=product_seller)
        return render(request,'seller_view_product.html',{'products':products})

def seller_edit_product(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
            product.product_name=request.POST['product_name']
            product.product_category=request.POST['product_category']
            product.product_size=request.POST['product_size']
            product.product_color=request.POST['product_color']
            product.product_price=request.POST['product_price']
            product.product_desc=request.POST['product_desc']
            try:
                product.product_image=request.FILES['product_image']
            except:
                pass
            product.save()
            msg="Product Edited Successfully"
            return render(request,'seller_edit_product.html',{'msg':msg,'product':product})
    else:
        return render(request,'seller_edit_product.html',{'product':product})
    
def seller_delete_product(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller_view_product')

def product_detail(request,pk):
    wishlist_flag=False
    cart_flag=False
    product=Product.objects.get(pk=pk)
    try:
        user=User.objects.get(email=request.session['email'])
    except:
        pass
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_flag=True
    except:
        pass
    try:
        Cart.objects.get(user=user,product=product,payment_status="pending")
        cart_flag=True
    except:
        pass
    return render(request,'product_detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})
        

def add_to_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(
        product=product,
        user=user
    )
    return redirect('wishlist')

def wishlist(request):
    try:
        user=User.objects.get(email=request.session['email'])
        wishlist=Wishlist.objects.filter(user=user)
        request.session['wishlist_count']=len(wishlist)
        return render(request,'wishlist.html',{'wishlist':wishlist})
    except:
        return redirect('login')

def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(product=product,user=user)
    wishlist.delete()
    return redirect('wishlist')

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        user=user,
        product=product,
        product_price=product.product_price,
        product_qty=1,
        total_price=product.product_price
    )
    return redirect('cart')

def cart(request):
    net_price=0
    try:
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user,payment_status="pending")
    except:
        return redirect('login')
    for i in cart:
        net_price=net_price+i.total_price
    request.session['cart_count']=len(cart)
    return render(request,'cart.html',{'cart':cart,'net_price':net_price})

def remove_from_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(product=product,user=user)
    cart.delete()
    return redirect('cart')

def change_qty(request):
    cart=Cart.objects.get(pk=request.POST['cid'])
    product_qty=int(request.POST['product_qty'])
    cart.product_qty=product_qty
    cart.total_price=cart.product_price*product_qty
    cart.save()
    return redirect('cart')

def my_orders(request):
    user=User.objects.get(email=request.session['email'])
    products=Cart.objects.filter(user=user,payment_status='paid')
    return render(request,'my_orders.html',{'products':products})

def search(request):
    products=Product.objects.filter(product_name__contains=request.POST['search'])
    print(request.POST['search'])
    msg="Search Result For "+"'"+request.POST['search']+"'"
    return render(request,'search.html',{'products':products,'msg':msg})

def seller_orders(request):
    seller=User.objects.get(email=request.session['email'])
    carts=Cart.objects.filter(payment_status='paid')
    products=[]
    for i in carts:
        if i.product.product_seller==seller:
            products.append(i)
    return render(request,'seller_orders.html',{'products':products})

def change_password(request):
    if request.method=='POST':
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST["cnew_password"]:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg='New Password And Confirm New Password Does Not Matched'
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg='Old Password Is Incorrect'
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
        except:
            msg='Email Not Registered'
            return render(request,'forgot_password.html',{'msg':msg})
        otp=random.randint(1000,9999)
        subject = 'OTP For Forgot Password'
        message = 'Hello'+user.fname+'your otp for forgot password is '+str(otp)+'.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'otp.html',{'otp':otp,'email':request.POST['email']})
    else:
        return render(request,'forgot_password.html')

def verify_otp(request):
    otp=request.POST['otp']
    uotp=request.POST['uotp']
    email=request.POST['email']

    if otp==uotp:
        return render(request,'new_password.html',{'email':email})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})

def new_password(request):
    email=request.POST['email']
    print(email)
    p=request.POST['new_password']
    cp=request.POST['cnew_password']
    if p==cp:
        user=User.objects.get(email=email)
        user.password=p
        user.save()
        msg='Password Changed Successfully'
        return render(request,'login.html',{'msg':msg})
    else:
        msg='New Password And Confirm New Password Not Matched'
        return render(request,'new_password.html',{'msg':msg})

def billing_details(request):
    amount=request.POST['amount']
    return render(request,'billing_details.html',{'amount':amount})

def profile(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        return redirect('index')
    return render(request,'profile.html',{'info':info})

def profile_update(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        pass
    try:
        info.fname=request.POST['fname']
        info.lname=request.POST['lname']
        info.email=request.POST['email']
        info.mobile=request.POST['mobile']
        info.address=request.POST['address']
        info.save()
    except:
        pass
    msg="Profile Updated Successfully"
    return render(request,'profile.html',{'info':info,'msg':msg})

def seller_profile(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        return redirect('index')
    return render(request,'seller_profile.html',{'info':info})

def seller_profile_update(request):
    try:
        info=User.objects.get(email=request.session['email'])
    except:
        pass
    try:
        info.fname=request.POST['fname']
        info.lname=request.POST['lname']
        info.email=request.POST['email']
        info.mobile=request.POST['mobile']
        info.address=request.POST['address']
        info.save()
    except:
        pass
    msg="Profile Updated Successfully"
    return render(request,'seller_profile.html',{'info':info,'msg':msg})

def seller_order_detail(request):
    return render(request,'seller_order_detail.html')