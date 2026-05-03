# Base class for model fields using descriptors
class Field:
    def __init__(self, column_type, nullable=False):
        self.column_type = column_type
        self.nullable = nullable

    # Store the field name on the instance
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    # Getter for descriptor
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    # Setter for descriptor with validation
    def __set__(self, instance, value):
        value = self.validate(value)
        setattr(instance, self.private_name, value)

    # Basic null check validation
    def validate(self, value):
        if not self.nullable and value is None:
            raise ValueError(f"{self.name} cannot be None")
        return value

    # Generate SQL for table creation
    def get_sql(self):
        sql = f"{self.name} {self.column_type}"
        if not self.nullable:
            sql += " NOT NULL"
        return sql

# Field for string values
class CharField(Field):
    def __init__(self, max_length):
        super().__init__(f"VARCHAR({max_length})")
        self.max_length = max_length

    # Validate string type and length
    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if value is not None and len(value) > self.max_length:
            raise ValueError(f"{self.name} exceeds max_length of {self.max_length}")
        return value

# Field for integer values
class IntegerField(Field):
    def __init__(self, nullable=False):
        super().__init__("INTEGER", nullable=nullable)

    # Validate integer type
    def validate(self, value):
        value = super().validate(value)
        if value is not None and not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")
        return value

# Handles reverse relationships (e.g., user.posts)
class ReverseRelation:
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.model.filter(**{f"{self.field_name}_id": instance.id})

# Field for linking models together
class ForeignKey(Field):
    def __init__(self, to, related_name=None):
        super().__init__("INTEGER")
        self.to = to
        self.related_name = related_name

    # Set up reverse relation if requested
    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self.private_name = f"_{name}_id"
        if self.related_name:
            setattr(self.to, self.related_name, ReverseRelation(owner, name))

    def get_sql(self):
        return f"{self.name}_id INTEGER"

    # Fetch the related object lazily
    def __get__(self, instance, owner):
        if instance is None:
            return self
        fk_id = getattr(instance, self.private_name, None)
        return None if fk_id is None else self.to.get(id=fk_id)

    # Store the ID of the related object
    def __set__(self, instance, value):
        if value is not None and not isinstance(value, self.to):
            raise TypeError(f"{self.name} must be an instance of {self.to.__name__}")
        setattr(instance, self.private_name, None if value is None else value.id)