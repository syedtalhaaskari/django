from pprint import pprint
from django.contrib.auth.models import User
from core.models import Restaurant, Rating, Sale
from django.utils import timezone
from django.db import connection

def run():
    # restaurant = Restaurant()
    # restaurant.name = 'My Italian Restaurant'
    # restaurant.latitude = 50.2
    # restaurant.longitude = 50.2
    # restaurant.date_opened = timezone.now()
    # restaurant.restaurant_type = Restaurant.TypeChoices.ITALIAN
    
    # restaurant.save()

    # restaurants = Restaurant.objects.all()
    # restaurants = Restaurant.objects.first()
    # restaurants = Restaurant.objects.last()
    # restaurant = Restaurant.objects.first()
    # restaurants = Restaurant.objects.all()[0]

    # print(restaurants)
    # print(restaurant)

    # Restaurant.objects.create(
    #     name="Pizza Shop",
    #     date_opened=timezone.now(),
    #     restaurant_type=Restaurant.TypeChoices.ITALIAN,
    #     latitude=40.7128,
    #     longitude=-74.0060,
    # )
    # user = User()
    # user.username = 'john_doe'
    # user.email = 'john@example.com'
    # user.first_name = 'John'
    # user.last_name = 'Doe'
    # user.password = 'password'
    # user.save()

    # restaurant = Restaurant.objects.last()
    # user = User.objects.first()

    # Rating.objects.create(
    #     user=user,
    #     restaurant=restaurant,
    #     rating=4
    # )

    # print(Rating.objects.all())
    # print(Rating.objects.filter(rating=3))
    # print(Rating.objects.filter(rating__gte=3))
    # print(Rating.objects.filter(rating__lte=3))
    # print(Rating.objects.filter(rating__lt=3))

    # print(Rating.objects.exclude(rating__lt=3))

    # restaurant = Restaurant.objects.first()
    # print(restaurant.name) 

    # restaurant.name = 'My Italian Restaurant'

    # restaurant.save()

    # rating = Rating.objects.first()
    # print(rating.restaurant.name)

    # restaurant = Restaurant.objects.last()
    # print(restaurant.ratings.all())

    # Sale.objects.create(
    #     restaurant=Restaurant.objects.first(),
    #     income=2.33,
    #     datetime=timezone.now()
    # )
    # Sale.objects.create(
    #     restaurant=Restaurant.objects.last(),
    #     income=5.33,
    #     datetime=timezone.now()
    # )
    # Sale.objects.create(
    #     restaurant=Restaurant.objects.first(),
    #     income=8.33,
    #     datetime=timezone.now()
    # )
    # restaurant = Restaurant.objects.first()
    # pprint(restaurant.sales.all())

    user = User.objects.first()
    restaurant = Restaurant.objects.first()

    rating, created = Rating.objects.get_or_create(
        restaurant=restaurant,
        user=user,
        rating=4
    )
    print(rating)
    print(created)

    pprint(connection.queries)