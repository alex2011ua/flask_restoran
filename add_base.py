import csv
from restoran.models import User, Category, Meal
from restoran import app, db

def add():

    with open("delivery_categories.csv", encoding = 'UTF-8') as f:
        read = csv.reader(f, delimiter=',')
        next(read)
        for row in read:
            category = Category()
            category.id = row[0]
            category.title = row[1]
            db.session.add(category)
        db.session.commit()

    with open("delivery_items.csv", encoding = 'UTF-8') as f:
        read = csv.reader(f, delimiter=',')
        next(read)
        for row in read:
            meal = Meal()
            meal.id = row[0]
            meal.title = row[1]
            meal.price = int(row[2])
            meal.description = row[3]
            meal.picture = row[4]
            meal.category_id = int(row[5])
            db.session.add(meal)
        db.session.commit()


    adm = User()

    adm.mail = 'admin'
    adm.password = 'admin'
    adm.role = 'admin'
    db.session.add(adm)

    user = User()

    user.mail = 'user'
    user.password = 'user'
    user.role = 'user'
    db.session.add(user)

    db.session.commit()