from typing import Optional, List, Dict, Any


class BookService:
    """In-memory book service with CRUD operations."""
    
    def __init__(self) -> None:
        """Initialize BookService with empty book list and ID counter."""
        self.books: List[Dict[str, Any]] = []
        self._next_id: int = 1
    
    def create_book(self, title: str, author: str) -> Dict[str, Any]:
        """Create a new book and return it with generated ID.
        
        Args:
            title: Book title (non-empty string)
            author: Book author (non-empty string)
            
        Returns:
            Dict containing book data with generated ID
            
        Raises:
            ValueError: If title or author is invalid
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
    
    def get_book(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a book by its ID.
        
        Args:
            book_id: Unique book identifier
            
        Returns:
            Book data dict if found, None otherwise
        """
        for book in self.books:
            if book["id"] == book_id:
                return book
        return None
    
    def list_books(self, search: Optional[str] = None, 
                   sort_by: Optional[str] = None, 
                   ascending: bool = True) -> List[Dict[str, Any]]:
        """List books with optional search and sorting.
        
        Args:
            search: Optional search term for title/author filtering
            sort_by: Field to sort by ('title', 'author', 'id')
            ascending: Sort direction (default: True)
            
        Returns:
            List of book dictionaries
            
        Raises:
            ValueError: If sort_by field is invalid
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
            valid_fields = {"id", "title", "author"}
            if sort_by not in valid_fields:
                raise ValueError(f"Invalid sort field: {sort_by}. Must be one of {valid_fields}")
            
            def sort_key(book):
                value = book[sort_by]
                if sort_by == "id":
                    return int(value)  # Sort IDs numerically
                return value.lower()  # Case-insensitive for strings
            
            result.sort(key=sort_key, reverse=not ascending)
        
        return result
    
    def delete_book(self, book_id: str) -> bool:
        """Delete a book by its ID.
        
        Args:
            book_id: Unique book identifier
            
        Returns:
            True if deleted, False if not found
        """
        for i, book in enumerate(self.books):
            if book["id"] == book_id:
                self.books.pop(i)
                return True
        return False
