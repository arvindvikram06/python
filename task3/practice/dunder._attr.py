class User:
    def __setattr__(self, name, value):
        print(f"Setting {name} = {value}")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        print(f"{name} not found, returning default")
        return None


u = User()

u.name = "Alice"   # triggers __setattr__
u.age = 25

print(u.name)      # normal access
print(u.email)     # triggers __getattr__