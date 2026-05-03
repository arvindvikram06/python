# Lightweight Python ORM

A custom-built Object-Relational Mapper (ORM) in **Python** and **SQLite** that provides a high-level abstraction for database operations

---

## Features

- **Declarative Model System**
  - Define database tables using Python classes inheriting from `Model`.
  - Supports various field types including `CharField`, `IntegerField`, and `ForeignKey`.

- **Automated Schema Generation**
  - Automatically creates SQLite tables based on class definitions.
  - Handles constraints like `max_length`, `nullable`, and `AUTOINCREMENT`.

- **Fluent Query API**
  - Implements a `QuerySet` pattern for chaining operations.
  - Supports filtering (e.g., `age__gte=25`), ordering (`order_by`), and retrieval.

- **Relationship Management**
  - Implements `ForeignKey` relationships with support for `related_name`.
  - Allows easy access to related objects (e.g., `user.posts.all()`).

- **CRUD Operations**
  - Simple `save()`, `delete()`, and `get()` methods for easy data management.

---

## Tech Stack

- **Python 3**
- **SQLite3**
- **Meta-programming** (Descriptors and class introspection)

---

## Project Workflow

1. **Model Definition**: Define your data structure using the `Model` and `Field` classes.
2. **Table Creation**: Call `create_table()` on your models to synchronize the database schema.
3. **Instance Management**: Create instances of your models and call `save()` to persist them to the database.
4. **Querying**: Use the `filter()` and `get()` class methods to search for data.
5. **Relationships**: Access related data through descriptors and reverse relationships.

---

## ORM Logic

- **Descriptors**: Used to manage field access and validation at the attribute level.
- **SQL Generation**: Dynamically builds SQL strings for `INSERT`, `SELECT`, and `DELETE` operations based on model attributes.
- **Query Chaining**: `QuerySet` objects store filter criteria and only execute the SQL query when `.all()` or `.first()` is called (Lazy evaluation).

---

## Installation

```bash
python app.py
```
