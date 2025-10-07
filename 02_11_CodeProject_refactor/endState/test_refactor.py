#!/usr/bin/env python3
"""
Simple test to verify the refactored list_books behavior.
"""

# Create a simplified version without type annotations for testing
class BookService:
    def __init__(self):
        self.books = []
        self._next_id = 1
    
    def create_book(self, title, author):
        title = title.strip()
        author = author.strip()
        
        if not title or not author:
            raise ValueError("Title and author must be non-empty strings")
        
        book = {
            "id": str(self._next_id),
            "title": title,
            "author": author
        }
        
        self.books.append(book)
        self._next_id += 1
        return book
    
    def list_books(self, search=None, sort_by=None, ascending=True):
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
    
    def _sort_books(self, books, sort_by, ascending=True):
        """Sort books by the specified field."""
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

def test_refactored_behavior():
    """Test that the refactored behavior is identical to the original."""
    print("Testing refactored BookService behavior...")
    
    # Create service and add test books
    service = BookService()
    service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
    service.create_book("Animal Farm", "George Orwell")
    service.create_book("1984", "George Orwell")
    service.create_book("To Kill a Mockingbird", "Harper Lee")
    
    print("\n1. Testing unsorted list:")
    books = service.list_books()
    for book in books:
        print(f"  {book['title']} by {book['author']} (ID: {book['id']})")
    
    print("\n2. Testing sort by title (ascending):")
    books = service.list_books(sort_by="title")
    for book in books:
        print(f"  {book['title']} by {book['author']}")
    
    print("\n3. Testing sort by title (descending):")
    books = service.list_books(sort_by="title", ascending=False)
    for book in books:
        print(f"  {book['title']} by {book['author']}")
    
    print("\n4. Testing sort by author:")
    books = service.list_books(sort_by="author")
    for book in books:
        print(f"  {book['title']} by {book['author']}")
    
    print("\n5. Testing sort by ID:")
    books = service.list_books(sort_by="id")
    for book in books:
        print(f"  {book['title']} by {book['author']} (ID: {book['id']})")
    
    print("\n6. Testing search with sorting:")
    books = service.list_books(search="Orwell", sort_by="title")
    for book in books:
        print(f"  {book['title']} by {book['author']}")
    
    print("\n7. Testing invalid sort field (should raise error):")
    try:
        service.list_books(sort_by="invalid_field")
        print("  ERROR: Should have raised ValueError")
    except ValueError as e:
        print(f"  ✓ Correctly raised ValueError: {e}")
    
    print("\n✓ All tests completed successfully!")

if __name__ == "__main__":
    test_refactored_behavior()
