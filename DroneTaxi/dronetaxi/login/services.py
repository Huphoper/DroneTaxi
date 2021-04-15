from .models import User, Order, Drone
from django.contrib.auth.hashers import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def login_user(login, password):
    try:
        user = User.objects.get(email=login)
        check_password(password, user.password)
        if check_password(password, user.password):
            return user
    except User.DoesNotExist:
        return None


def registration(lastname, firstname, patronymic, email, password, confpassword):
    try:
        validate_email(email)
    except ValidationError:
        return 'notmail'
    if len(password) < 8:
        return 'smallpass'
    try:
        if password != confpassword:
            return 'passerror'
        basepassword = make_password(password)
        userfind = User.objects.get(email=email)
        if userfind != userfind.DoesNotExist:
            return 'mailerror'
    except User.DoesNotExist:
        User.objects.create(lastname=lastname, firstname=firstname, patronymic=patronymic, email=email,
                            password=basepassword)


def getUserWithEmail(email):
    return User.objects.get(email=email)


def orderslist(user):
    if User.objects.get(email=user).user_role == 'opr':
        list = Order.objects.all().order_by('order_status', 'order_time')
        return list
    else:
        list = Order.objects.filter(client=user).order_by('order_status', 'order_time')
        return list


def userslist():
    users = User.objects.all()
    return users


def droneslist():
    drones = Drone.objects.all()
    return drones


def operatorlist():
    operators = User.objects.filter(user_role='opr')
    return operators


def clientlist():
    clients = User.objects.filter(user_role='clt')
    return clients


def freedronelist(order_id):
    droneclass = Order.objects.get(id=order_id).drone_class
    freedrones = Drone.objects.filter(drone_status='fre', drone_class=droneclass)
    return freedrones


def profileedit(editor, entered_lastname, entered_firstname, entered_patronymic,
                serialized_user,
                entered_password, entered_confpassword, entered_phone_number, entered_role):
    if entered_password != entered_confpassword:
        return 'passerror'
    if len(entered_password) < 8:
        return 'smallpass'
    basepassword = make_password(entered_password)
    if User.objects.get(email=editor).user_role == 'adm':
        User.objects.filter(email=serialized_user).update(lastname=entered_lastname, firstname=entered_firstname,
                                                          patronymic=entered_patronymic,
                                                          password=basepassword, phone_number=entered_phone_number,
                                                          user_role=entered_role)
    else:
        User.objects.filter(email=serialized_user).update(lastname=entered_lastname, firstname=entered_firstname,
                                                          patronymic=entered_patronymic,
                                                          password=basepassword, phone_number=entered_phone_number,
                                                          )


def droneinfo(id):
    drone = Drone.objects.filter(id=id)
    return drone


def orderinfo(id, serialized_user):
    order = Order.objects.filter(id=id)
    operator = Order.objects.get(id=id).operator
    editor = User.objects.get(email=serialized_user)
    if operator is None and editor.user_role == 'opr':
        Order.objects.filter(id=id).update(operator=editor)
    return order


def droneedit(id, entered_drone_brand, entered_drone_model, entered_production_year,
              entered_registration_number, entered_registration_date, entered_drone_status,
              entered_drone_image, entered_drone_class):
    Drone.objects.filter(id=id).update(drone_brand=entered_drone_brand, drone_model=entered_drone_model,
                                       production_year=entered_production_year,
                                       registration_number=entered_registration_number,
                                       registration_date=entered_registration_date, drone_status=entered_drone_status,
                                       drone_image=entered_drone_image, drone_class=entered_drone_class)

    return 'data'


def getuserrole(mail):
    role = User.objects.get(email=mail).user_role
    return role


def orderedit(order_id, entered_order_status, entered_drone):
    Order.objects.filter(id=order_id).update(order_status=entered_order_status, drone=entered_drone)
    if entered_order_status == 'per':
        print(entered_drone)
        print('123')
        Drone.objects.filter(id=entered_drone).update(drone_status='bsy')
    else:
        print(entered_drone, 123)
        print('123')
        Drone.objects.filter(id=entered_drone).update(drone_status='fre')


def orderupdate(order_id, entered_order_status):
    Order.objects.filter(id=order_id).update(order_status=entered_order_status)
    if entered_order_status == 'per':
        drone = Order.objects.get(id=order_id).drone.id
        Drone.objects.filter(id=drone).update(drone_status='bsy')
    else:
        drone = Order.objects.get(id=order_id).drone.id
        Drone.objects.filter(id=drone).update(drone_status='fre')


def useradd(entered_lastname, entered_firstname, entered_patronymic, entered_email, entered_userrole,
            entered_phone_number,
            entered_password, entered_confpassword):

    try:
        validate_email(entered_email)
    except ValidationError:
        return 'notmail'
    if len(entered_password) < 8:
        return 'smallpass'
    try:
        if entered_password != entered_confpassword:
            return 'passerror'
        userfind = User.objects.get(email=entered_email)
        if userfind != userfind.DoesNotExist:
            return 'mailerror'

    except User.DoesNotExist:
        basepassword = make_password(entered_password)
        User.objects.create(lastname=entered_lastname, firstname=entered_firstname, patronymic=entered_patronymic,
                            email=entered_email, phone_number=entered_phone_number,
                            password=basepassword, user_role=entered_userrole)


def droneadd(entered_drone_brand, entered_drone_model, entered_production_year,
             entered_registration_number, entered_registration_date, entered_drone_status,
             entered_drone_image, entered_drone_class):
    Drone.objects.create(drone_brand=entered_drone_brand, drone_model=entered_drone_model,
                         production_year=entered_production_year,
                         registration_number=entered_registration_number,
                         registration_date=entered_registration_date,
                         drone_status=entered_drone_status,
                         drone_image=entered_drone_image,
                         drone_class=entered_drone_class)


def orderadd(entered_order_time, entered_departure_point, entered_arrival_place,
             entered_cost, entered_order_status, entered_drone_class,
             entered_client):
    user = User.objects.get(email=entered_client)
    Order.objects.create(order_time=entered_order_time, departure_point=entered_departure_point,
                         arrival_place=entered_arrival_place,
                         cost=entered_cost,
                         order_status=entered_order_status,
                         drone_class=entered_drone_class,
                         client=user)


def getfullname(email):
    try:
        fullname = User.objects.get(email=email).lastname.firstname.patronymic
        return fullname
    except User.DoesNotExist:
        return None
