"""
BookService: In-memory book management with CRUD operations.

This module provides a simple in-memory book service for managing a collection
of books with basic CRUD (Create, Read, Update, Delete) operations. The service
supports creating books with titles and authors, retrieving books by ID,
listing books with optional search and sorting, and deleting books.

Methods:
    create_book(title, author): Create a new book with auto-generated ID
    get_book(book_id): Retrieve a book by its unique ID
    list_books(search=None, sort_by=None, ascending=True): List books with optional filtering and sorting
    delete_book(book_id): Remove a book from the collection

Usage Example:
    from book_service import BookService
    
    # Create service instance
    service = BookService()
    
    # Add some books
    book1 = service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
    book2 = service.create_book("To Kill a Mockingbird", "Harper Lee")
    
    # Search and sort books
    gatsby_books = service.list_books(search="Gatsby")
    sorted_books = service.list_books(sort_by="title", ascending=True)
    
    # Retrieve specific book
    book = service.get_book(book1["id"])
    
    # Delete a book
    service.delete_book(book2["id"])
"""



class BookService:
    """In-memory book service with CRUD operations."""
    
    def __init__(self) -> None:
        """Initialize BookService with empty book list and ID counter.
        
        Initializes a new BookService instance with an empty list of books
        and sets the next available ID to 1.
        """
        self.books: list[dict[str, str]] = []
        self._next_id: int = 1
    
    def create_book(self, title: str, author: str) -> dict[str, str]:
        """Create a new book and return it with generated ID.
        
        Creates a new book entry with the provided title and author. The book
        is assigned a unique auto-generated ID and added to the service's
        collection.
        
        Args:
            title: The title of the book. Must be a non-empty string after
                whitespace is stripped.
            author: The author of the book. Must be a non-empty string after
                whitespace is stripped.
        
        Returns:
            A dictionary containing the book data with keys 'id', 'title', and
            'author'. The 'id' is a string representation of the auto-generated
            unique identifier.
        
        Raises:
            ValueError: If either title or author is empty or contains only
                whitespace after stripping.
        
        Example:
            >>> service = BookService()
            >>> book = service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
            >>> print(book['id'])
            '1'
            >>> print(book['title'])
            'The Great Gatsby'
        """
        # Strip whitespace and validate
        title = title.strip()
        author = author.strip()
        
        if not title or not author:
            raise ValueError("Title and author must be non-empty strings")
        
        # Create book dict
        book = {
            "id": str(self._next_id),
            "title": title,
            "author": author
        }
        
        # Add to list and increment counter
        self.books.append(book)
        self._next_id += 1
        
        return book
    
    def get_book(self, book_id: str) -> dict[str, str] | None:
        """Retrieve a book by its unique identifier.
        
        Searches the book collection for a book with the specified ID and
        returns its data if found.
        
        Args:
            book_id: The unique string identifier of the book to retrieve.
        
        Returns:
            A dictionary containing the book data with keys 'id', 'title', and
            'author' if the book is found, otherwise None.
        
        Example:
            >>> service = BookService()
            >>> service.create_book("1984", "George Orwell")
            {'id': '1', 'title': '1984', 'author': 'George Orwell'}
            >>> book = service.get_book('1')
            >>> print(book['title'])
            1984
            >>> service.get_book('999')
            None
        """
        for book in self.books:
            if book["id"] == book_id:
                return book
        return None
    
    def list_books(self, search: str | None = None, 
                   sort_by: str | None = None, 
                   ascending: bool = True) -> list[dict[str, str]]:
        """List books with optional search filtering and sorting.
        
        Returns a list of all books in the service, optionally filtered by
        a search term and sorted by a specified field.
        
        Args:
            search: Optional search term to filter books by. Searches both
                title and author fields (case-insensitive). If None, no
                filtering is applied.
            sort_by: Optional field name to sort by. Valid values are 'title',
                'author', or 'id'. If None, no sorting is applied.
            ascending: Sort direction when sort_by is specified. True for
                ascending order, False for descending order. Defaults to True.
        
        Returns:
            A list of dictionaries, each containing book data with keys 'id',
            'title', and 'author'. The list may be filtered and/or sorted
            based on the provided parameters.
        
        Raises:
            ValueError: If sort_by is specified but not one of the valid
                field names ('title', 'author', 'id').
        
        Example:
            >>> service = BookService()
            >>> service.create_book("1984", "George Orwell")
            >>> service.create_book("Animal Farm", "George Orwell")
            >>> service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
            >>> # List all books
            >>> all_books = service.list_books()
            >>> # Search for Orwell books
            >>> orwell_books = service.list_books(search="Orwell")
            >>> # Sort by title
            >>> sorted_books = service.list_books(sort_by="title")
        """
        # Start with all books
        result = self.books.copy()
        
        # Filter by search if provided
        if search:
            search_lower = search.lower()
            result = [
                book for book in result 
                if search_lower in book["title"].lower() or 
                   search_lower in book["author"].lower()
            ]
        
        # Sort if sort_by is provided
        if sort_by:
            result = self._sort_books(result, sort_by, ascending)
        
        return result
    
    def _sort_books(self, books: list[dict[str, str]], 
                   sort_by: str, ascending: bool = True) -> list[dict[str, str]]:
        """Sort books by the specified field.
        
        Helper method to sort a list of books by a given field with optional
        sort direction. Handles both string and numeric sorting appropriately.
        
        Args:
            books: List of book dictionaries to sort
            sort_by: Field name to sort by ('id', 'title', or 'author')
            ascending: Sort direction - True for ascending, False for descending
        
        Returns:
            A new list of books sorted by the specified field
        
        Raises:
            ValueError: If sort_by is not one of the valid field names
        """
        valid_fields = {"id", "title", "author"}
        if sort_by not in valid_fields:
            raise ValueError(f"Invalid sort field: {sort_by}. Must be one of {valid_fields}")
        
        def sort_key(book):
            value = book[sort_by]
            if sort_by == "id":
                return int(value)  # Sort IDs numerically
            return value.lower()  # Case-insensitive for strings
        
        sorted_books = books.copy()
        sorted_books.sort(key=sort_key, reverse=not ascending)
        return sorted_books
    
    def delete_book(self, book_id: str) -> bool:
        """Delete a book from the collection by its unique identifier.
        
        Removes the book with the specified ID from the service's collection.
        The book is permanently removed and cannot be recovered.
        
        Args:
            book_id: The unique string identifier of the book to delete.
        
        Returns:
            True if the book was found and successfully deleted, False if
            no book with the specified ID was found.
        
        Example:
            >>> service = BookService()
            >>> service.create_book("1984", "George Orwell")
            {'id': '1', 'title': '1984', 'author': 'George Orwell'}
            >>> service.delete_book('1')
            True
            >>> service.delete_book('999')
            False
            >>> service.get_book('1')
            None
        """
        for i, book in enumerate(self.books):
            if book["id"] == book_id:
                self.books.pop(i)
                return True
        return False


def demo() -> None:
    """Demonstrate BookService functionality with basic CRUD operations."""
    # Create BookService instance
    service = BookService()
    
    # Create two books
    book1 = service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
    book2 = service.create_book("To Kill a Mockingbird", "Harper Lee")
    
    # Get the first book
    retrieved_book = service.get_book(book1["id"])
    assert retrieved_book is not None, "First book should be retrievable"
    assert retrieved_book["title"] == "The Great Gatsby", "Retrieved book should have correct title"
    assert retrieved_book["author"] == "F. Scott Fitzgerald", "Retrieved book should have correct author"
    
    # List all books
    all_books = service.list_books()
    assert len(all_books) == 2, "Should have 2 books total"
    assert book1 in all_books, "First book should be in the list"
    assert book2 in all_books, "Second book should be in the list"
    
    # Delete one book and verify it's gone
    delete_result = service.delete_book(book1["id"])
    assert delete_result is True, "Book deletion should return True"
    
    # Verify the book is gone
    deleted_book = service.get_book(book1["id"])
    assert deleted_book is None, "Deleted book should not be retrievable"
    
    # Verify only one book remains
    remaining_books = service.list_books()
    assert len(remaining_books) == 1, "Should have 1 book remaining"
    assert book2 in remaining_books, "Second book should still be in the list"
    assert book1 not in remaining_books, "First book should not be in the list"
    
    print("Demo completed successfully! All assertions passed.")


if __name__ == "__main__":
    demo()
