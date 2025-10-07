# Book Service Project

This readme file is a reference for the Coding Project in Chapter 2, Video 6 "Coding Project - Speed up python coding with smart prompts". You can compare your work to the completed file in this directory labeled "book_service_endState.py".

We'll start with the shape of the class: method names, arguments, return types. Then we'll fill in the details together.

## Getting Started

### Step 1: Class Structure

I'm going to use this prompt:

```
Generate a Python class called BookService with four methods: create_book(title, author), get_book(book_id), list_books(search?, sort_by?, ascending?), and delete_book(book_id). Just return type hints and docstrings for now — no implementation.
```

### Step 2: Constructor

We'll start with the constructor. Every service needs state. We'll store books in a list and keep a counter for the next ID.

I'll now use this prompt:

```
Implement the constructor for BookService so it initializes an empty list of books and a counter _next_id starting at 1.
```

### Step 3: Create Book Method

Next, we're going to implement the `create_book` method. We need validation since the title and author can't be empty, then assign an ID, store the book, and return it. This time we'll use a more detailed prompt:

```
Implement create_book so it:
- Validates that title and author are non-empty strings after stripping whitespace.
- Raises ValueError if invalid.
- Creates a dict with id, title, and author.
- Appends it to the internal list.
- Increments the counter
- Returns the dict.
```

### Step 4: Remaining Methods

I'll leave the remaining functions for you to implement:

- `get_book(book_id)` - Retrieve a book by its ID
- `list_books(search?, sort_by?, ascending?)` - List books with optional search and sorting
- `delete_book(book_id)` - Remove a book by its ID
