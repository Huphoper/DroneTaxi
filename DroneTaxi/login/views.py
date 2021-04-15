from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .forms import UserForm
from .models import User
from django.views import View
from . import services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


class UseraccountViewSet(View):
    queryset = User.objects.all()


def login(request):
    if request.method == "POST":
        entered_email = request.POST.get("login")
        entered_password = request.POST.get("password")
        entered_rem = request.POST.get("remember")

        user = services.login_user(entered_email, entered_password)
        if user is not None:
            request.session['email'] = entered_email
            request.session['role'] = services.getuserrole(entered_email)
            request.session['remember'] = entered_rem
            return HttpResponseRedirect("/profile")
        else:

            return render(request, "login/login.html", {"error": True, "login": entered_email})
    else:

        if request.session.get('remember') == 'on':
            log = request.session['email']
            request.session['email'] = ''
        else:
            log = ''
            request.session['email'] = ''

        return render(request, "login/login.html", {"login": log})


def registration(request):
    if request.method == "GET":
        return render(request, "login/registration.html")
    if request.method == "POST":
        entered_lastname = request.POST.get("lastname")
        entered_firstname = request.POST.get("firstname")
        entered_patronymic = request.POST.get("patronymic")
        entered_email = request.POST.get("email")
        entered_password = request.POST.get("password")
        entered_confpassword = request.POST.get("confpassword")
        user = services.registration(entered_lastname, entered_firstname, entered_patronymic, entered_email,
                                     entered_password, entered_confpassword)
        if user == "mailerror":
            return render(request, "login/registration.html",
                          {"mailerror": True, "lastname": entered_lastname, "firstname": entered_firstname,
                           "patronymic": entered_patronymic,
                           "email": entered_email, "password": entered_password, "confpassword": entered_confpassword})
        if user == "passerror":
            return render(request, "login/registration.html",
                          {"passerror": True, "lastname": entered_lastname, "firstname": entered_firstname,
                           "patronymic": entered_patronymic,
                           "email": entered_email, "password": entered_password, "confpassword": entered_confpassword})
        if user == "notmail":
            return render(request, "login/registration.html",
                          {"notmail": True, "lastname": entered_lastname, "firstname": entered_firstname,
                           "patronymic": entered_patronymic,
                           "email": entered_email, "password": entered_password, "confpassword": entered_confpassword})
        if user == "smallpass":
            return render(request, "login/registration.html",
                          {"smallpass": True, "lastname": entered_lastname, "firstname": entered_firstname,
                           "patronymic": entered_patronymic,
                           "email": entered_email, "password": entered_password, "confpassword": entered_confpassword})

        request.session['email'] = entered_email
        request.session['role'] = 'clt'
        return HttpResponseRedirect("/profile")


def profile(request):
    email = request.session.get('email')
    role = request.session.get('role')
    if email is not None:
        try:
            serialized_user = email
            user = services.getUserWithEmail(serialized_user)
        except User.DoesNotExist:
            return HttpResponseRedirect("/login")

        data_context = {"user_context": serialized_user, "user": user, "role": role, "title": "Drone Taxi - Профиль"}
        return render(request, "userprofile/profile.html", context=data_context)
    else:
        return HttpResponseRedirect("/login")


def myorders(request):
    email = request.session.get('email')
    role = request.session.get('role')
    if email is not None:
        try:
            serialized_user = email
            orders = services.orderslist(serialized_user)
        except User.DoesNotExist:
            return HttpResponseRedirect("/login")
        paginator = Paginator(orders, 5)

        page = request.GET.get('page')
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            orders = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            orders = paginator.page(paginator.num_pages)
        count = len(orders)
        data_context = {"user_context": serialized_user, "orders": orders, "role": role, "count": count,
                        "title": "Drone Taxi - Мои заказы"}
        return render(request, "order/orderlist.html", context=data_context)
    else:
        return HttpResponseRedirect("/login")


def userslist(request):
    email = request.session.get('email')
    role = request.session.get('role')
    if email is not None:
        if role != 'adm':
            return HttpResponseRedirect("/profile")
        try:
            serialized_user = email
            users = services.userslist()
        except User.DoesNotExist:
            return HttpResponseRedirect("/login")
        paginator = Paginator(users, 5)

        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            users = paginator.page(paginator.num_pages)

        data_context = {"user_context": serialized_user, "users": users, "role": role,
                        "title": "Drone Taxi - Список пользователей"}
        return render(request, "userprofile/userlist.html", context=data_context)
    else:
        return HttpResponseRedirect("/login")


def droneslist(request):
    email = request.session.get('email')
    role = request.session.get('role')
    if email is not None:
        if role == 'clt':
            return HttpResponseRedirect("/profile")
        try:
            serialized_user = email
            drones = services.droneslist()
        except User.DoesNotExist:
            return HttpResponseRedirect("/login")
        paginator = Paginator(drones, 4)

        page = request.GET.get('page')
        try:
            drones = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            drones = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            drones = paginator.page(paginator.num_pages)
        count = len(drones)
        data_context = {"user_context": serialized_user, "drones": drones, "role": role, "count": count,
                        "title": "Drone Taxi - Список дронов"}
        return render(request, "drone/dronelist.html", context=data_context)
    else:
        return HttpResponseRedirect("/login")


def orderedit(request):
    email = request.session.get('email')
    role = request.session.get('role')
    try:
        if email is not None:
            serialized_user = email
            if request.method == "POST":
                val = request.POST.get("addval")
                if val is not None:
                    order_id = request.POST.get("orderid")
                    entered_order_status = request.POST.get("order_status")
                    if entered_order_status == 'Отменен':
                        entered_order_status = 'can'
                    elif entered_order_status == 'Закрыт':
                        entered_order_status = 'cls'
                    elif entered_order_status == 'Исполняется':
                        entered_order_status = 'per'
                    elif entered_order_status == 'Активен':
                        entered_order_status = 'act'
                    entered_drone = request.POST.get("drone")
                    if entered_drone is not None:
                        services.orderedit(order_id, entered_order_status, entered_drone)
                    else:
                        services.orderupdate(order_id, entered_order_status)

                    return HttpResponseRedirect("/myorders")
                else:
                    order_id = request.POST.get("orderid")
                    order = services.orderinfo(order_id, serialized_user)
                    freedrones = services.freedronelist(order_id)
                    data_context = {"user_context": serialized_user, "order": order, "role": role,
                                    "freedrones": freedrones, "title": "Drone Taxi - Редактирование заказа"}
                    return render(request, "order/orderedit.html", context=data_context)
        else:
            return HttpResponseRedirect("/login")
    except User.DoesNotExist:
        return HttpResponseRedirect("/login")


def droneedit(request):
    email = request.session.get('email')
    role = request.session.get('role')
    try:
        if email is not None:
            serialized_user = email
            if role != 'adm':
                return HttpResponseRedirect("/profile")

            if request.method == "POST":
                val = request.POST.get("addval")
                if val is not None:
                    drone_id = request.POST.get("droneid")
                    entered_drone_brand = request.POST.get("drone_brand")
                    entered_drone_model = request.POST.get("drone_model")
                    entered_production_year = request.POST.get("production_year")
                    entered_registration_number = request.POST.get("registration_number")
                    entered_registration_date = request.POST.get("registration_date")
                    entered_drone_status = request.POST.get("drone_status")
                    if entered_drone_status == 'Занят':
                        entered_drone_status = 'bsy'
                    elif entered_drone_status == 'Свободен':
                        entered_drone_status = 'fre'
                    entered_drone_image = request.POST.get("drone_image")
                    entered_drone_class = request.POST.get("drone_class")
                    if entered_drone_class == 'Эконом':
                        entered_drone_class = 'eco'
                    elif entered_drone_class == 'Бизнес':
                        entered_drone_class = 'bus'
                    elif entered_drone_class == 'Премиум':
                        entered_drone_class = 'pre'

                    try:
                        drone = services.droneinfo(drone_id)

                        entered_production_year = int(entered_production_year)

                        if entered_production_year < 2018:
                            return render(request, "drone/droneedit.html",
                                          {"user_context": serialized_user, "role": role, "drone": drone,
                                           "tooold": True, "title": "Drone Taxi - Редактирование дрона"})
                    except ValueError:
                        return render(request, "drone/droneedit.html",
                                      {"user_context": serialized_user, "role": role, "drone": drone, "notdate": True,
                                       "title": "Drone Taxi - Редактирование дрона"})
                    err = services.droneedit(drone_id, entered_drone_brand, entered_drone_model,
                                             entered_production_year,
                                             entered_registration_number, entered_registration_date,
                                             entered_drone_status,
                                             entered_drone_image, entered_drone_class)
                    if err == "passerror":
                        return render(request, "drone/droneedit.html", {"passerror": True, "role": role,
                                                                        "title": "Drone Taxi - Редактирование дрона"})
                    else:
                        return HttpResponseRedirect("/droneslist")
                else:
                    drone_id = request.POST.get("droneid")
                    drone = services.droneinfo(drone_id)
                    data_context = {"user_context": serialized_user, "drone": drone, "role": role,
                                    "title": "Drone Taxi - Редактирование дрона"}
                    return render(request, "drone/droneedit.html", context=data_context)
        else:
            return HttpResponseRedirect("/login")
    except User.DoesNotExist:
        return HttpResponseRedirect("/login")


def editprofile(request):
    email = request.session.get('email')
    role = request.session.get('role')
    try:
        if email is not None:
            serialized_user = email
            user = services.getUserWithEmail(serialized_user)
            if request.method == "POST":
                val = request.POST.get("addval")
                mail = request.POST.get("userid")
                user = services.getUserWithEmail(mail)
                if val is not None:
                    entered_lastname = request.POST.get("lastname")
                    entered_firstname = request.POST.get("firstname")
                    entered_patronymic = request.POST.get("patronymic")
                    entered_password = request.POST.get("password")
                    entered_confpassword = request.POST.get("confpassword")
                    entered_phone_number = request.POST.get("phone_number")
                    entered_role = request.POST.get("user_role")

                    if entered_role == 'Администратор':
                        entered_role = 'adm'
                    elif entered_role == 'Клиент':
                        entered_role = 'clt'
                    elif entered_role == 'Оператор':
                        entered_role = 'opr'
                    err = services.profileedit(serialized_user, entered_lastname, entered_firstname, entered_patronymic,
                                               mail,
                                               entered_password, entered_confpassword, entered_phone_number,
                                               entered_role)
                    if err == 'smallpass':
                        return render(request, "userprofile/profileedit.html",
                                      {"user_context": serialized_user, "user": user, "role": role, "smallpass": True,
                                       "title": "Drone Taxi - Редактирование профиля"})

                    if err == "passerror":
                        data_context = {"user_context": serialized_user, "user": user, "passerror": True, "role": role,
                                        "title": "Drone Taxi - Редактирование профиля"}
                        return render(request, "userprofile/profileedit.html", context=data_context)
                    else:
                        return HttpResponseRedirect("/userslist")
            else:
                data_context = {"user_context": serialized_user, "user": user, "role": role,
                                "title": "Drone Taxi - Редактирование профиля"}
                return render(request, "userprofile/profileedit.html", context=data_context)

            data_context = {"user_context": serialized_user, "user": user, "role": role,
                            "title": "Drone Taxi - Редактирование профиля"}
            return render(request, "userprofile/profileedit.html", context=data_context)
        else:
            return HttpResponseRedirect("/login")
    except User.DoesNotExist:
        return HttpResponseRedirect("/login")


def droneadd(request):
    email = request.session.get('email')
    role = request.session.get('role')
    serialized_user = email
    try:
        if email is not None:
            if role != 'adm':
                return HttpResponseRedirect("/profile")

            if request.method == "POST":
                entered_drone_brand = request.POST.get("drone_brand")
                entered_drone_model = request.POST.get("drone_model")
                entered_production_year = request.POST.get("production_year")

                entered_registration_number = request.POST.get("registration_number")
                entered_registration_date = request.POST.get("registration_date")
                entered_drone_status = 'fre'
                entered_drone_image = request.POST.get("drone_image")
                entered_drone_class = request.POST.get("drone_class")
                if entered_drone_class == 'Эконом':
                    entered_drone_class = 'eco'
                elif entered_drone_class == 'Бизнес':
                    entered_drone_class = 'bus'
                elif entered_drone_class == 'Премиум':
                    entered_drone_class = 'pre'
                try:
                    entered_production_year = int(entered_production_year)
                    if entered_production_year < 2018:
                        return render(request, "drone/droneadd.html",
                                      {"user_context": serialized_user, "role": role, "tooold": True,
                                       "drone_brand": entered_drone_brand,
                                       "drone_model": entered_drone_model, "production_year": entered_production_year,
                                       "registration_number": entered_registration_number,
                                       "title": "Drone Taxi - Добавление дрона"})
                except ValueError:
                    return render(request, "drone/droneadd.html",
                                  {"user_context": serialized_user, "role": role, "notdate": True,
                                   "drone_brand": entered_drone_brand,
                                   "drone_model": entered_drone_model, "production_year": entered_production_year,
                                   "registration_number": entered_registration_number,
                                   "title": "Drone Taxi - Добавление дрона"})

                err = services.droneadd(entered_drone_brand, entered_drone_model, entered_production_year,
                                        entered_registration_number, entered_registration_date, entered_drone_status,
                                        entered_drone_image, entered_drone_class)
                return HttpResponseRedirect("/droneslist")
            else:
                return render(request, "drone/droneadd.html", {"user_context": serialized_user, "role": role,
                                                               "title": "Drone Taxi - Добавление дрона"})
        else:
            return HttpResponseRedirect("/login")
    except User.DoesNotExist:
        return HttpResponseRedirect("/login")


def useradd(request):
    email = request.session.get('email')
    role = request.session.get('role')
    try:

        if email is not None:
            serialized_user = email
            if role != 'adm':
                return HttpResponseRedirect("/profile")
            if request.method == "POST":

                entered_lastname = request.POST.get("lastname")
                entered_firstname = request.POST.get("firstname")
                entered_patronymic = request.POST.get("patronymic")
                entered_email = request.POST.get("email")
                entered_password = request.POST.get("password")
                entered_confpassword = request.POST.get("confpassword")
                entered_userrole = request.POST.get("user_role")
                if entered_userrole == 'Администратор':
                    entered_userrole = 'adm'
                elif entered_userrole == 'Клиент':
                    entered_userrole = 'clt'
                elif entered_userrole == 'Оператор':
                    entered_userrole = 'opr'
                entered_phone_number = request.POST.get("phone_number")
                user = services.useradd(entered_lastname, entered_firstname, entered_patronymic, entered_email,
                                        entered_userrole, entered_phone_number,
                                        entered_password, entered_confpassword)
                if user == "mailerror":
                    return render(request, "userprofile/useradd.html",
                                  {"mailerror": True, "role": role, "lastname": entered_lastname,
                                   "firstname": entered_firstname, "patronymic": entered_patronymic,
                                   "email": entered_email, "password": entered_password,
                                   "phone_number": entered_phone_number,
                                   "confpassword": entered_confpassword, "title": "Drone Taxi - Создание пользователя"})
                if user == "passerror":
                    return render(request, "userprofile/useradd.html",
                                  {"passerror": True, "role": role, "lastname": entered_lastname,
                                   "firstname": entered_firstname, "patronymic": entered_patronymic,
                                   "email": entered_email, "password": entered_password,
                                   "phone_number": entered_phone_number,
                                   "confpassword": entered_confpassword, "title": "Drone Taxi - Создание пользователя"})
                if user == 'smallpass':
                    return render(request, "userprofile/useradd.html",
                                  {"smallpass": True, "role": role, "lastname": entered_lastname,
                                   "firstname": entered_firstname, "patronymic": entered_patronymic,
                                   "email": entered_email, "password": entered_password,
                                   "phone_number": entered_phone_number,
                                   "confpassword": entered_confpassword, "title": "Drone Taxi - Создание пользователя"})
                if user == "notmail":
                    return render(request, "userprofile/useradd.html",
                                  {"notmail": True, "role": role, "lastname": entered_lastname,
                                   "firstname": entered_firstname, "patronymic": entered_patronymic,
                                   "email": entered_email, "password": entered_password,
                                   "phone_number": entered_phone_number,
                                   "confpassword": entered_confpassword, "title": "Drone Taxi - Создание пользователя"})
                return HttpResponseRedirect("/userslist")
            else:
                return render(request, "userprofile/useradd.html", {"user_context": serialized_user, "role": role,
                                                                    "title": "Drone Taxi - Создание пользователя"})
        else:
            return HttpResponseRedirect("/login")
    except User.DoesNotExist:
        return HttpResponseRedirect("/login")


def orderadd(request):
    email = request.session.get('email')
    role = request.session.get('role')
    try:

        if email is not None:
            if role == 'adm':
                return HttpResponseRedirect("/profile")
            if request.method == "POST":
                entered_order_time = request.POST.get("order_time")
                entered_departure_point = request.POST.get("departure_point")
                entered_arrival_place = request.POST.get("arrival_place")
                entered_cost = 500
                entered_order_status = 'act'
                entered_drone_class = request.POST.get("drone_class")
                if entered_drone_class == 'Эконом':
                    entered_drone_class = 'eco'
                    entered_cost = 500
                elif entered_drone_class == 'Бизнес':
                    entered_drone_class = 'bus'
                    entered_cost = 1000
                elif entered_drone_class == 'Премиум':
                    entered_drone_class = 'pre'
                    entered_cost = 1500
                entered_client = request.POST.get("client")
                print(datetime.now())
                entered_order_time = entered_order_time.replace('T', ' ')
                if datetime.strptime(entered_order_time, "%Y-%m-%d %H:%M") < datetime.now():
                    return render(request, "order/orderadd.html", {"role": role,
                                                                   "email": email, "dataerror": True,
                                                                   "departure_point": entered_departure_point,
                                                                   "arrival_place": entered_arrival_place,
                                                                   "title": "Drone Taxi - Оформление заказа"})

                err = services.orderadd(entered_order_time, entered_departure_point, entered_arrival_place,
                                        entered_cost, entered_order_status, entered_drone_class,
                                        entered_client)
                return HttpResponseRedirect("/myorders")
            else:

                return render(request, "order/orderadd.html", {"role": role,
                                                               "email": email,
                                                               "title": "Drone Taxi - Оформление заказа"})
        else:
            return HttpResponseRedirect("/login")
    except User.DoesNotExist:
        return HttpResponseRedirect("/login")


def Custom_handler404(request, exception):
    return HttpResponseNotFound("main/error404", {"title": "Drone Taxi - Ошибка 404"})
