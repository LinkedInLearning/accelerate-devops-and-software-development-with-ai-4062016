import pytest
from book_service import BookService


class TestBookServiceCreate:
    """Test create_book method edge cases."""
    
    def test_create_valid_books(self):
        """Test creating valid books."""
        service = BookService()
        book1 = service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
        book2 = service.create_book("To Kill a Mockingbird", "Harper Lee")
        
        assert book1["title"] == "The Great Gatsby"
        assert book1["author"] == "F. Scott Fitzgerald"
        assert book1["id"] == "1"
        assert book2["id"] == "2"
        assert len(service.books) == 2
    
    @pytest.mark.parametrize("title,author", [
        ("", "Author"),
        ("Title", ""),
        ("   ", "Author"),
        ("Title", "   "),
        ("", ""),
        ("   ", "   "),
    ])
    def test_create_empty_strings(self, title, author):
        """Test creating books with empty or whitespace-only strings."""
        service = BookService()
        with pytest.raises(ValueError, match="Title and author must be non-empty strings"):
            service.create_book(title, author)
    
    @pytest.mark.parametrize("title,author", [
        (None, "Author"),
        ("Title", None),
        (123, "Author"),
        ("Title", 456),
        ([], "Author"),
        ("Title", {}),
    ])
    def test_create_invalid_types(self, title, author):
        """Test creating books with invalid input types."""
        service = BookService()
        with pytest.raises((TypeError, ValueError)):
            service.create_book(title, author)
    
    def test_create_whitespace_stripping(self):
        """Test that whitespace is properly stripped."""
        service = BookService()
        book = service.create_book("  The Great Gatsby  ", "  F. Scott Fitzgerald  ")
        
        assert book["title"] == "The Great Gatsby"
        assert book["author"] == "F. Scott Fitzgerald"
    
    def test_create_unicode_characters(self):
        """Test creating books with Unicode characters."""
        service = BookService()
        book = service.create_book("Café", "José María")
        
        assert book["title"] == "Café"
        assert book["author"] == "José María"
    
    def test_create_duplicate_titles_authors(self):
        """Test creating books with duplicate titles and authors."""
        service = BookService()
        book1 = service.create_book("The Book", "Author")
        book2 = service.create_book("The Book", "Author")
        
        assert book1["id"] == "1"
        assert book2["id"] == "2"
        assert len(service.books) == 2


class TestBookServiceGet:
    """Test get_book method edge cases."""
    
    def test_get_existing_book(self):
        """Test getting an existing book."""
        service = BookService()
        book = service.create_book("Test Book", "Test Author")
        retrieved = service.get_book(book["id"])
        
        assert retrieved == book
    
    @pytest.mark.parametrize("book_id", [
        "999",
        "0",
        "-1",
        "",
        "   ",
        None,
        123,
        [],
        {},
    ])
    def test_get_nonexistent_book(self, book_id):
        """Test getting non-existent books."""
        service = BookService()
        service.create_book("Test Book", "Test Author")
        result = service.get_book(book_id)
        
        assert result is None
    
    def test_get_after_deletion(self):
        """Test getting a book after it's been deleted."""
        service = BookService()
        book = service.create_book("Test Book", "Test Author")
        service.delete_book(book["id"])
        result = service.get_book(book["id"])
        
        assert result is None


class TestBookServiceList:
    """Test list_books method edge cases."""
    
    def test_list_empty_service(self):
        """Test listing books from empty service."""
        service = BookService()
        books = service.list_books()
        
        assert books == []
    
    def test_list_all_books(self):
        """Test listing all books."""
        service = BookService()
        book1 = service.create_book("Book A", "Author A")
        book2 = service.create_book("Book B", "Author B")
        books = service.list_books()
        
        assert len(books) == 2
        assert book1 in books
        assert book2 in books
    
    @pytest.mark.parametrize("search_term,expected_count", [
        ("book", 2),
        ("BOOK", 2),
        ("Book A", 1),
        ("Author A", 1),
        ("nonexistent", 0),
        ("", 2),
        ("   ", 0),
    ])
    def test_list_search(self, search_term, expected_count):
        """Test searching books."""
        service = BookService()
        service.create_book("Book A", "Author A")
        service.create_book("Book B", "Author B")
        books = service.list_books(search=search_term)
        
        assert len(books) == expected_count
    
    def test_list_search_unicode(self):
        """Test searching with Unicode characters."""
        service = BookService()
        service.create_book("Café", "José")
        books = service.list_books(search="café")
        
        assert len(books) == 1
        assert books[0]["title"] == "Café"
    
    @pytest.mark.parametrize("sort_by,ascending,expected_order", [
        ("id", True, ["1", "2", "3"]),
        ("id", False, ["3", "2", "1"]),
        ("title", True, ["A Book", "B Book", "C Book"]),
        ("title", False, ["C Book", "B Book", "A Book"]),
        ("author", True, ["Author A", "Author B", "Author C"]),
        ("author", False, ["Author C", "Author B", "Author A"]),
    ])
    def test_list_sorting(self, sort_by, ascending, expected_order):
        """Test sorting books by different fields and directions."""
        service = BookService()
        service.create_book("C Book", "Author C")
        service.create_book("A Book", "Author A")
        service.create_book("B Book", "Author B")
        
        books = service.list_books(sort_by=sort_by, ascending=ascending)
        actual_order = [book[sort_by] for book in books]
        
        assert actual_order == expected_order
    
    def test_list_sort_stability(self):
        """Test that sorting is stable for identical values."""
        service = BookService()
        book1 = service.create_book("Same Title", "Author A")
        book2 = service.create_book("Same Title", "Author B")
        
        books = service.list_books(sort_by="title", ascending=True)
        # Should maintain original order for identical titles
        assert books[0]["author"] == "Author A"
        assert books[1]["author"] == "Author B"
    
    @pytest.mark.parametrize("sort_by", [
        "invalid_field",
        "price",
        "year",
        "",
        None,
        123,
    ])
    def test_list_invalid_sort_field(self, sort_by):
        """Test listing with invalid sort fields."""
        service = BookService()
        service.create_book("Test Book", "Test Author")
        
        with pytest.raises(ValueError):
            service.list_books(sort_by=sort_by)
    
    def test_list_combined_search_sort(self):
        """Test combining search and sort."""
        service = BookService()
        service.create_book("Book A", "Author A")
        service.create_book("Book B", "Author B")
        service.create_book("Book C", "Author C")
        
        books = service.list_books(search="Book", sort_by="title", ascending=False)
        titles = [book["title"] for book in books]
        
        assert titles == ["Book C", "Book B", "Book A"]


class TestBookServiceDelete:
    """Test delete_book method edge cases."""
    
    def test_delete_existing_book(self):
        """Test deleting an existing book."""
        service = BookService()
        book = service.create_book("Test Book", "Test Author")
        result = service.delete_book(book["id"])
        
        assert result is True
        assert len(service.books) == 0
        assert service.get_book(book["id"]) is None
    
    @pytest.mark.parametrize("book_id", [
        "999",
        "0",
        "-1",
        "",
        "   ",
        None,
        123,
        [],
        {},
    ])
    def test_delete_nonexistent_book(self, book_id):
        """Test deleting non-existent books."""
        service = BookService()
        service.create_book("Test Book", "Test Author")
        result = service.delete_book(book_id)
        
        assert result is False
        assert len(service.books) == 1
    
    def test_delete_idempotency(self):
        """Test that deleting the same book twice is idempotent."""
        service = BookService()
        book = service.create_book("Test Book", "Test Author")
        
        # First deletion
        result1 = service.delete_book(book["id"])
        assert result1 is True
        assert len(service.books) == 0
        
        # Second deletion
        result2 = service.delete_book(book["id"])
        assert result2 is False
        assert len(service.books) == 0
    
    def test_delete_specific_book(self):
        """Test that deleting one book doesn't affect others."""
        service = BookService()
        book1 = service.create_book("Book 1", "Author 1")
        book2 = service.create_book("Book 2", "Author 2")
        
        service.delete_book(book1["id"])
        
        assert len(service.books) == 1
        assert service.get_book(book2["id"]) == book2
        assert service.get_book(book1["id"]) is None


class TestBookServiceIntegration:
    """Test integration scenarios and complex workflows."""
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow."""
        service = BookService()
        
        # Create
        book = service.create_book("Test Book", "Test Author")
        assert book["id"] == "1"
        
        # Read
        retrieved = service.get_book(book["id"])
        assert retrieved == book
        
        # List
        books = service.list_books()
        assert len(books) == 1
        assert book in books
        
        # Update (simulated by delete + create)
        service.delete_book(book["id"])
        updated_book = service.create_book("Updated Book", "Updated Author")
        assert updated_book["id"] == "2"
        
        # Delete
        result = service.delete_book(updated_book["id"])
        assert result is True
        assert len(service.books) == 0
    
    def test_large_dataset(self):
        """Test with a larger dataset."""
        service = BookService()
        
        # Create many books
        books = []
        for i in range(100):
            book = service.create_book(f"Book {i}", f"Author {i}")
            books.append(book)
        
        assert len(service.books) == 100
        
        # Test search performance
        search_results = service.list_books(search="Book 5")
        assert len(search_results) == 1
        
        # Test sort performance
        sorted_books = service.list_books(sort_by="title", ascending=True)
        assert len(sorted_books) == 100
        assert sorted_books[0]["title"] == "Book 0"
        assert sorted_books[-1]["title"] == "Book 99"
        
        # Test delete performance
        service.delete_book(books[50]["id"])
        assert len(service.books) == 99
    
    def test_unicode_handling(self):
        """Test comprehensive Unicode handling."""
        service = BookService()
        
        unicode_books = [
            ("Café", "José María"),
            ("naïve", "François"),
            ("résumé", "André"),
            ("中文", "作者"),
            ("العربية", "كاتب"),
            ("русский", "автор"),
        ]
        
        for title, author in unicode_books:
            book = service.create_book(title, author)
            assert book["title"] == title
            assert book["author"] == author
        
        # Test search with Unicode
        results = service.list_books(search="café")
        assert len(results) == 1
        assert results[0]["title"] == "Café"
        
        # Test sort with Unicode
        sorted_books = service.list_books(sort_by="title", ascending=True)
        assert len(sorted_books) == len(unicode_books)
    
    def test_edge_case_whitespace(self):
        """Test various whitespace edge cases."""
        service = BookService()
        
        # Test whitespace in search
        service.create_book("The Great Gatsby", "F. Scott Fitzgerald")
        results = service.list_books(search="  gatsby  ")
        assert len(results) == 1
        
        # Test empty search
        results = service.list_books(search="")
        assert len(results) == 1
        
        # Test whitespace-only search
        results = service.list_books(search="   ")
        assert len(results) == 0
    
    def test_id_generation_sequence(self):
        """Test ID generation sequence and uniqueness."""
        service = BookService()
        
        # Create and delete books to test ID sequence
        book1 = service.create_book("Book 1", "Author 1")
        book2 = service.create_book("Book 2", "Author 2")
        book3 = service.create_book("Book 3", "Author 3")
        
        assert book1["id"] == "1"
        assert book2["id"] == "2"
        assert book3["id"] == "3"
        
        # Delete middle book
        service.delete_book(book2["id"])
        
        # Create new book - should get next ID
        book4 = service.create_book("Book 4", "Author 4")
        assert book4["id"] == "4"
        
        # Verify all IDs are unique
        all_books = service.list_books()
        ids = [book["id"] for book in all_books]
        assert len(set(ids)) == len(ids)  # All unique


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
