from database import connect
from model import Model
from fields import CharField, IntegerField, ForeignKey

connect()

class User(Model):
    name  = CharField(max_length=100)
    email = CharField(max_length=255)
    age   = IntegerField(nullable=True)


class Post(Model):
    title  = CharField(max_length=200)
    author = ForeignKey(User, related_name="posts")


User.create_table()
Post.create_table()

u = User(name="Arvind", email="arvind@gmail.com", age=30)
u.save()

p = Post(title="Hello", author=u)
p.save()


# print(p.author)


posts = u.posts.all()
for post in posts:
    print(post)


users = User.filter(age__gte=25).order_by("-name").all()
for user in users:
    print(user.name)