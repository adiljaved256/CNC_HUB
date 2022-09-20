from django.shortcuts import render
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from passlib.hash import django_pbkdf2_sha256 as handler
from sendemail.models import *
import sendemail.usable as uc
from decouple import config
import random
import jwt

# send_mail Api
class Email_sending(APIView):
        def post(self, request):
            email = request.POST.get('email')
            oTP = request.POST.get('oTP')
            # print('email------------------------',email)

            code = random.randint(99999,999999)

            send_mail(
                'forget email',f'forget token:{code}','muhammadadil436huh@gmail.com',
                [email]
            )

            objcode =  account.objects.filter(email=email).first()
            if  objcode:
                objcode.oTP=code
                objcode.oTPStatus=True
                objcode.save()
                return Response({"status":True,"message":"Email send Successfully!"})
################################################################################################################################################################

# Account Signup-API

class accounts(APIView):
    def post(self,request):                                                                                                                         
        firstname =request.data.get("firstname")
        lastname = request.data.get("lastname")
        address = request.data.get("address")
        password=request.data.get('password')
        email=request.data.get('email')
        ContactNo =request.data.get('ContactNo')
                                       
        data = account(firstname=firstname,lastname=lastname,password= handler.hash(password),email = email, 
        ContactNo=ContactNo)
        data.save()

        return Response({"status":True,"message":"Account Created Successfully"},201)
 
# =================================================================================================

# Account login-API

class login(APIView):

    def post (self,request):

        email = request.data.get('email')
        password = request.data.get('password')

        fetchAccount = account.objects.filter(email=email).first()
        if fetchAccount:
            if handler.verify(password,fetchAccount.password):
                
                    access_token_payload = {
                                    'id': fetchAccount.id,
                                    'firstname':fetchAccount.firstname, 
                                    'email':fetchAccount.email, 

                            }

                    access_token = jwt.encode(access_token_payload,config('accountkey'),algorithm = 'HS256')
                    data = {'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'email':fetchAccount.email, 'ContactNo':fetchAccount. ContactNo 
               }

                    return Response({"status":True,"message":"Login Successlly","token":access_token,"accountdata":data},200)

   
            else:
                return Response({"status":False,"message":"Invalid crediatials"},200)

        else:
            return Response({"status":False,"message":"Account doesnot access"}) 

# ===================================================================================================================

# verify code_Api

class  verifycode(APIView):
        def post(self,request):
            code=request.data.get('code')
            email=request.data.get('email')

            objverify =  account.objects.filter(email=email).first()
            
            if objverify:
                if (objverify.oTP==int(code)):

                    objverify.oTPStatus='True'
                    objverify.save()
                    return Response({"status":True, 'Msg':' VerifIcation Is True'})      
                else:
                    return Response({"status":False,  'Msg':'Invalid Code'})    
            else:
                return Response({"status":False,  'Msg':'Account doesnot Exists'})

#+====================================================================================================================
# change password_Api
class  changepassword(APIView):
    def post(self,request): 
        password=request.data.get('password')
        newpassword=request.data.get('newpassword')
        email=request.data.get('email')
        
        changepassword =  account.objects.filter(email=email).first()

        if changepassword:
            if changepassword.oTPStatus=='True':
            
                changepassword.password= handler.hash(newpassword)
                
                changepassword.oTPStatus='False'

                changepassword.save()

                return Response({"status":True,"message":"Password Change Successfully!"})
        
            else:
        
                return Response({"status":False,  'Msg':'code Expired'})               
        else:
            return Response({"status":False,  'Msg':'Work is not done'})                           
        