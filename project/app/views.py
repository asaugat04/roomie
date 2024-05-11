from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile, Room, RoomRequest
from django.contrib.auth import authenticate, login, logout
import base64
import uuid
from django.core.files.base import ContentFile

@login_required
def home(request):
    return render(request,"app/home.html")



def signup(request):

    if request.method == "POST":
        form_data = request.POST

        username = form_data["user_name"]
        try:
            user = User.objects.get(username=username)
            messages.error(request, "Username already exists. Please try with another username.")
            return redirect("app:signup")
        except:
            password = form_data["password"]
            first_name = form_data["first_name"]
            last_name = form_data["last_name"]

            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)


            current_address = form_data["current_address"]
            permanent_address = form_data["permanent_address"]
            contact_no = form_data["contact_no"]

            gender = form_data["gender"]
            food_pref = form_data["food_pref"]
            user_type_1 = form_data["user_type_1"]
            user_type_2 = form_data["user_type_2"]
            interests = form_data["interests"]

            Profile.objects.create(
                user=user,
                temp_address=current_address,
                perm_address=permanent_address,
                phone_no=contact_no,
                gender=gender,
                food_preference=food_pref,
                user_type=user_type_1,
                user_type_2=user_type_2,
                interests=interests
                
            )
            messages.success(request, "Account created successfully. Please login.")
            return redirect("app:login")


    return render(request,"app/signup.html")



def user_login(request):
    if request.method == "POST":
        form_data = request.POST
        username = form_data["user_name"]
        password = form_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("app:home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("app:login")

    return render(request,"app/login.html")




@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect("app:login")




@login_required
def profile(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        "profile": profile
    }
    return render(request,"app/profile.html", context)


@login_required
def update_profile_pic(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        profile.image = request.FILES['user_image']
        profile.save()
        messages.success(request, "Profile picture updated successfully.")
    return redirect("app:profile")


@login_required
def offer_room(request):
    if request.method=="POST":

        # Assuming the base64 data is in the 'image' field of the request
        base64_data = request.POST['previewImage']

        # Remove the prefix from the base64 data
        base64_data = base64_data.split(',')[-1]

        # Decode the base64 data
        decoded_data = base64.b64decode(base64_data)

        # Create a file object
        file_object = ContentFile(decoded_data, name=f'{uuid.uuid4()}.png')

        location = request.POST['location']
        price = request.POST['price']
        roommate_max_capacity = request.POST['roommate-max-capacity']

        Room.objects.create(
            location=location,
            price=price,
            roommate_max_capacity=roommate_max_capacity,
            image=file_object,
            listed_by=request.user
        )

        return redirect("app:home")
        

    return render(request,"app/offer_room.html")



@login_required
def rooms(request):

    if request.session.get("location"):
        rooms = Room.objects.filter(location__icontains=request.session.get("location"))
        request.session["location"] = None

    else:
        rooms = Room.objects.all()

    requests = RoomRequest.objects.filter(profile=request.user.profile)
    requested_rooms = []
    for r in requests:
        if r.room in rooms:
            requested_rooms.append(r.room)

    context = {
        "rooms": rooms,
        "rooms_listed_by_this_user":rooms.filter(listed_by=request.user),
        "requested_rooms": requested_rooms
    }

    
    return render(request,"app/rooms.html", context)




@login_required
def roommates(request):
    roommates = Profile.objects.exclude(user=request.user)

    filtered_roommates = []
    for roommate in roommates:
        
        if roommate.gender == request.user.profile.gender:
            new_roommate = {
                "mate": roommate,
                "match_score": 0
            }
            filtered_roommates.append(new_roommate)

            if roommate.food_preference == request.user.profile.food_preference:
                filtered_roommates[-1]["match_score"] += 3
            if roommate.temp_address == request.user.profile.temp_address:
                filtered_roommates[-1]["match_score"] += 5
            if roommate.perm_address == request.user.profile.perm_address:
                filtered_roommates[-1]["match_score"] += 2
            if roommate.user_type == request.user.profile.user_type:
                filtered_roommates[-1]["match_score"] += 1
            if roommate.user_type_2 == request.user.profile.user_type_2:
                filtered_roommates[-1]["match_score"] += 2


    
    sorted_roommates = sorted(filtered_roommates, key=lambda x: x["match_score"], reverse=True)





        



    context = {
        "roommates": sorted_roommates
    }
    return render(request,"app/roommates.html", context)




@login_required
def show_profile(request, username):
    profile = Profile.objects.get(user__username=username)
    context = {
        "profile": profile
    }
    return render(request,"app/show_profile.html", context)




@login_required
def search(request):
    search_location = request.GET.get("location")
    request.session["location"] = search_location


    print(search_location, request.session.get("location"))

    return redirect("app:rooms")




@login_required
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    users_that_lives_in_this_room = Profile.objects.filter(lives_in=room)
    for user_profile in users_that_lives_in_this_room:
        user_profile.lives_in = None
        user_profile.save()

    room.delete()


    return redirect("app:rooms")




@login_required
def live_in(request, room_id):
    room = Room.objects.get(id=room_id)

    if room.roommate_max_capacity != 0:
        user_profile = Profile.objects.get(user=request.user)
        


        if user_profile.lives_in == room:
            return redirect("app:rooms")

        else:

            user_profile.lives_in = room
            user_profile.save()

            room.roommate_max_capacity -= 1
            room.save()

            return redirect("app:rooms")
    else:
        return redirect("app:rooms")




@login_required
def request_room(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user


    RoomRequest.objects.create(
        profile=user.profile,
        room=room
    )

    messages.success(request, "Request sent successfully.")

    return redirect("app:rooms")





@login_required
def room_detail(request, room_id):

    room = Room.objects.get(id=room_id)
    context = {
        "room": room,
        "requests": RoomRequest.objects.filter(room=room).filter(profile=request.user.profile)
    }
    return render(request,"app/room_detail.html", context)