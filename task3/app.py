from database import connect
from model import Model
from fields import CharField, IntegerField
from relationships import ForeignKey

# connect DB
connect()

# models
class User(Model):
    name = CharField(max_length=100)
    email = CharField(max_length=255)
    age = IntegerField(nullable=True)


# class Post(Model):
#     title = CharField(max_length=200)
#     author = ForeignKey(User, related_name="posts")


# User.create_table()

# u = User(name="arvind",email="arvindvikram47@gmail.com",age=30)
# u.save()


# u.name = "arvind"

# # create tables
# User.create_table()
# Post.create_table()


# # query
# users = User.filter(age__gte=25).order_by("-name").all()
# print(users)

# # relationship
# print(u.posts.all())