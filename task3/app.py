from database import connect
from model import Model
from fields import CharField, IntegerField, ForeignKey

# 1. Connect to DB
connect()

# 2. Define Models
class User(Model):
    name  = CharField(max_length=100)
    email = CharField(max_length=255)
    age   = IntegerField(nullable=True)

class Post(Model):
    title  = CharField(max_length=200)
    author = ForeignKey(User, related_name="posts")

# 3. Create Tables
User.create_table()
Post.create_table()

# 4. Create and Save Data
u = User(name="Arvind", email="arvind@gmail.com", age=30)
u.save()

p = Post(title="Hello World", author=u)
p.save()

# 5. Query and Use Relationships
print("\nUser's posts:")
for post in u.posts.all():
    print(f" - {post.title}")

print("\nFiltered Users:")
for user in User.filter(age__gte=25).order_by("-name").all():
    print(f" - {user.name}")