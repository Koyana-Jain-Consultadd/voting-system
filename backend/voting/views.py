from django.shortcuts import render,redirect
from rest_framework.views import APIView,Response
from voting.models import *
from django.contrib.auth.hashers import check_password
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
def verify_token(access_token):
    try:
        # Decode the access token using the secret key
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        
        # Check if the user exists in the database
        try:
            user = User.objects.get(u_id=user_id)
            return user
        except ObjectDoesNotExist:
            return None
        
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None
    

def userSignup(request):
    
    response={}
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        email=data.get('email')
        phone=data.get('phone')
        gender=data.get('gender')
        dob=data.get('dob')
        password=data.get('password')
        adhar_num=data.get('adhar_num')
        user_img=request.FILES.get('user_img')

        obj=User.objects.create(name=name, email=email, phone=phone, dob=dob, gender=gender, password=password, adhar_num=adhar_num, user_img=user_img, is_approved=False)
        obj.save()

        response={
            "success": True,
            "message": "User registered successfully"
        }
    return render(request, "signup.html", response)

def userLogin(request):
    
    if request.method == 'GET' and request.GET.get('success') == 'true':
        # If the success parameter is present in the URL, display the success alert
        message = "Registration successful. You can now log in."
        return render(request, 'userlogin.html', {'message': message, 'success': True})
   
    elif request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        user = User.objects.filter(email=email).first()
        if not user:
            
            response = {
                "success": False,
                "message": "User does not exist",
            }
            return render(request, "userlogin.html", response)

        if user.is_approved:  # Check if the user is approved
            if email == user.email and check_password(password, user.password):
                
                # Generate JWT token
                token_payload = {
                    "user_id": user.u_id,  # Assuming user id is stored in 'id' field
                }
                token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
                
                
                verified_user = verify_token(token)
                if verified_user:
                    
                    return redirect(f'/home?user_id={user.u_id}&access_token={token}')
                else:
                    
                    response = {
                        "success": False,
                        "message": "Invalid token",
                    }
                    return render(request, "userlogin.html", response)
                
            else:
                
                response = {
                    "success": False,
                    "message": "Invalid credentials",
                }
                return render(request, "userlogin.html", response)
        else:
            
            response = {
                "success": False,
                "message": "Your account approval is pending. Please contact the admin.",
            }
            return render(request, "userlogin.html", response)

    return render(request, "userlogin.html")

def home_view(request):
    access_token = request.GET.get('access_token')
    if request.method == 'POST':
        selected_e_id = request.POST.get('election')  # Get the selected election id from the form
        # Redirect to the voting panel with both user_id and access_token
        
        return HttpResponseRedirect(f'/votingpanel?selected_e_id={selected_e_id}&user_id={request.GET.get("user_id")}&access_token={access_token}')
    
    # If it's a GET request, retrieve user_id and access_token from the query parameters
    user_id = request.GET.get('user_id')
   
    if user_id:
        user = User.objects.filter(u_id=user_id).first()
        if user and verify_token(access_token):
            elections = Election.objects.all()
            context = {
                'elections': elections,
                'user': user,
                'access_token': access_token,
            }
            return render(request, 'home.html', context)

    # Handle the case when user_id is not provided or user does not exist
    return render(request, 'home.html', {'error_message': 'User not found, invalid user ID, or invalid token'})

def getUserId(request):
    access_token = request.GET.get('access_token')
    if access_token:
        try:
            decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            return user_id
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except jwt.InvalidTokenError:
            # Handle invalid token
            return None
    else:
        return None
    

def votingpanel(request):
    user_id = getUserId(request)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        candidate_id = request.POST.get('candidate_id')
        if candidate_id:
            try:
                result = Result.objects.get(candidate_id=candidate_id)
                result.votes += 1  # Increment the vote count
                result.save()
                return JsonResponse({'success': True})
            except Result.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Candidate not found'})
        else:
            return JsonResponse({'success': False, 'error': 'Candidate ID not provided'})
    else:
        selected_e_id = request.GET.get('selected_e_id')
        if selected_e_id:
            results = Result.objects.filter(election_id=selected_e_id)
            election_name = results.first().election.e_name
            return render(request, 'votingpanel.html', {'results': results, 'e_name': election_name, 'user_id': user_id})
        else:
            # Handle the case when the selected election ID is not provided
            return render(request, 'votingpanel.html', {'user_id': user_id})
        

def userLogout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    # Redirect to the login page
    return redirect('login')