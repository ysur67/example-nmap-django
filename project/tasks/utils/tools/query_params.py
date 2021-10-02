from drf_yasg import openapi

start_param = openapi.Parameter('Начало списка, включительно', in_=openapi.IN_QUERY,
                                description='Ид записи, с которой будет произведена выборка',
                                type=openapi.TYPE_INTEGER)

length_param = openapi.Parameter('Длина списка', in_=openapi.IN_QUERY,
                                 description='Число записей в выборке', type=openapi.TYPE_INTEGER)
