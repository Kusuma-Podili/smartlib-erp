package com.library.erp.service;

import com.library.erp.dto.catalog.BookRequestDto;
import com.library.erp.entity.Book;
import com.library.erp.entity.BookCopy;
import com.library.erp.entity.enums.BookStatus;
import com.library.erp.entity.enums.CopyCondition;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

public interface BookService {
    Book createBook(BookRequestDto dto);
    Book updateBook(Long id, BookRequestDto dto);
    List<BookCopy> addCopies(Long bookId, int count, CopyCondition condition);
    Book updateStatus(Long id, BookStatus status);
    Optional<Book> findById(Long id);
    Optional<Book> findByIsbn(String isbn);
    Page<Book> searchBooks(String keyword, Long categoryId, Long authorId, Long publisherId,
                           String language, BookStatus status, Boolean availableOnly, Pageable pageable);
    long countTotalBooks();
    long countAvailableBooks();
    void deleteBook(Long id);
}
