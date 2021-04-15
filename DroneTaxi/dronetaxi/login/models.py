from django.db import models


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)
    lastname = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=20, blank=True)
    STATUS = (('adm', 'Администратор'), ('clt', 'Клиент'), ('opr', 'Оператор'))
    user_role = models.CharField(max_length=3, choices=STATUS, default='clt', verbose_name="Роль пользователя")

    class Meta:
        ordering = ['email']
        verbose_name = 'Аккаунт пользователя'
        verbose_name_plural = "Аккаунты пользователей"

    def __str__(self):
        return f'{self.email}'


class Drone(models.Model):
    drone_brand = models.CharField(max_length=150)
    drone_model = models.CharField(max_length=150)
    production_year = models.IntegerField(default=2020)
    registration_number = models.CharField(max_length=8)
    registration_date = models.DateField(verbose_name="Дата регистрации")
    STATUS = (('fre', 'Свободен'), ('bsy', 'Занят'), ('wri', 'Списан'))
    drone_status = models.CharField(max_length=3, choices=STATUS, default='fre', verbose_name="Статус дрона")
    drone_image = models.ImageField(upload_to="static/image", verbose_name="Фото дрона")
    CLASS = (('eco', 'Эконом'), ('bus', 'Бизнес'), ('pre', 'Премиум'))
    drone_class = models.CharField(max_length=3, choices=CLASS, default='eco', verbose_name='Класс дрона')

    class Meta:
        verbose_name = 'Дрон'
        verbose_name_plural = "Дроны"

    def __str__(self):
        return f'{self.drone_brand}'


class Order(models.Model):
    order_time = models.DateTimeField(verbose_name="Дата заказа")
    departure_point = models.CharField(max_length=255)
    arrival_place = models.CharField(max_length=255)
    cost = models.FloatField(verbose_name='Стоимость заказа')
    STATUS = (('can', 'Отменен'), ('cls', 'Закрыт'), ('per', 'Исполняется'), ('act', 'Активен'))
    order_status = models.CharField(max_length=3, choices=STATUS, default='act', verbose_name="Статус заказа")
    CLASS = (('eco', 'Эконом'), ('bus', 'Бизнес'), ('pre', 'Премиум'))
    drone_class = models.CharField(max_length=3, choices=CLASS, default='eco', verbose_name='Класс дрона')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'{self.client} {self.order_status}'
