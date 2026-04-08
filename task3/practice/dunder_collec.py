class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return iter(self.items)


cart = Cart()
cart.add("Book")
cart.add("Pen")
cart.add("Bag")

print(len(cart))     # 3
print(cart[0])       # Book

for item in cart:
    print(item)