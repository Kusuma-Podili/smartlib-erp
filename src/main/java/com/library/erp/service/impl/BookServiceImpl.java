package com.library.erp.service.impl;

import com.library.erp.dto.catalog.BookRequestDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.BookStatus;
import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.entity.enums.CopyStatus;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.*;
import com.library.erp.service.BookService;
import com.library.erp.specification.BookSpecification;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class BookServiceImpl implements BookService {

    private final BookRepository bookRepository;
    private final BookCopyRepository bookCopyRepository;
    private final CategoryRepository categoryRepository;
    private final PublisherRepository publisherRepository;
    private final AuthorRepository authorRepository;

    @Override
    public Book createBook(BookRequestDto dto) {
        String cleanIsbn = dto.getIsbn().replaceAll("[\\s-]", "");
        if (bookRepository.existsByIsbn(cleanIsbn)) {
            throw new DuplicateResourceException("A book with ISBN " + cleanIsbn + " already exists in catalog.");
        }

        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + dto.getCategoryId()));

        Publisher publisher = publisherRepository.findById(dto.getPublisherId())
                .orElseThrow(() -> new ResourceNotFoundException("Publisher not found with id: " + dto.getPublisherId()));

        Set<Author> authors = new HashSet<>(authorRepository.findAllById(dto.getAuthorIds()));
        if (authors.isEmpty()) {
            throw new ResourceNotFoundException("No valid authors found for provided IDs.");
        }

        Book book = Book.builder()
                .isbn(cleanIsbn)
                .title(dto.getTitle().trim())
                .subtitle(dto.getSubtitle())
                .category(category)
                .publisher(publisher)
                .authors(authors)
                .edition(dto.getEdition())
                .publicationYear(dto.getPublicationYear())
                .language(dto.getLanguage() != null && !dto.getLanguage().isBlank() ? dto.getLanguage() : "English")
                .description(dto.getDescription())
                .coverImageUrl(dto.getCoverImageUrl())
                .shelfNumber(dto.getShelfNumber())
                .rackNumber(dto.getRackNumber())
                .price(dto.getPrice())
                .status(BookStatus.ACTIVE)
                .build();

        Book savedBook = bookRepository.save(book);

        // Generate initial physical copies
        int copiesToGenerate = dto.getInitialCopies() != null && dto.getInitialCopies() > 0 ? dto.getInitialCopies() : 1;
        List<BookCopy> copies = new ArrayList<>();
        for (int i = 1; i <= copiesToGenerate; i++) {
            String barcode = String.format("BC-%s-%03d", cleanIsbn, i);
            BookCopy copy = BookCopy.builder()
                    .book(savedBook)
                    .barcode(barcode)
                    .copyNumber(i)
                    .conditionStatus(CopyCondition.NEW)
                    .availabilityStatus(CopyStatus.AVAILABLE)
                    .acquiredDate(LocalDate.now())
                    .remarks("Initial catalog acquisition")
                    .build();
            copies.add(copy);
        }
        bookCopyRepository.saveAll(copies);
        savedBook.setCopies(copies);

        log.info("Successfully cataloged book '{}' (ISBN: {}) with {} physical copies.",
                savedBook.getTitle(), savedBook.getIsbn(), copiesToGenerate);

        return savedBook;
    }

    @Override
    public Book updateBook(Long id, BookRequestDto dto) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));

        String cleanIsbn = dto.getIsbn().replaceAll("[\\s-]", "");
        if (!book.getIsbn().equals(cleanIsbn) && bookRepository.existsByIsbn(cleanIsbn)) {
            throw new DuplicateResourceException("Another book already uses ISBN: " + cleanIsbn);
        }

        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + dto.getCategoryId()));

        Publisher publisher = publisherRepository.findById(dto.getPublisherId())
                .orElseThrow(() -> new ResourceNotFoundException("Publisher not found with id: " + dto.getPublisherId()));

        Set<Author> authors = new HashSet<>(authorRepository.findAllById(dto.getAuthorIds()));

        book.setIsbn(cleanIsbn);
        book.setTitle(dto.getTitle().trim());
        book.setSubtitle(dto.getSubtitle());
        book.setCategory(category);
        book.setPublisher(publisher);
        book.setAuthors(authors);
        book.setEdition(dto.getEdition());
        book.setPublicationYear(dto.getPublicationYear());
        book.setLanguage(dto.getLanguage());
        book.setDescription(dto.getDescription());
        book.setCoverImageUrl(dto.getCoverImageUrl());
        book.setShelfNumber(dto.getShelfNumber());
        book.setRackNumber(dto.getRackNumber());
        book.setPrice(dto.getPrice());

        return bookRepository.save(book);
    }

    @Override
    public List<BookCopy> addCopies(Long bookId, int count, CopyCondition condition) {
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + bookId));

        Integer maxCopyNumber = bookCopyRepository.findMaxCopyNumberByBookId(bookId);
        int startingNumber = (maxCopyNumber != null ? maxCopyNumber : 0) + 1;

        List<BookCopy> newCopies = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            int copyNum = startingNumber + i;
            String barcode = String.format("BC-%s-%03d", book.getIsbn(), copyNum);
            BookCopy copy = BookCopy.builder()
                    .book(book)
                    .barcode(barcode)
                    .copyNumber(copyNum)
                    .conditionStatus(condition != null ? condition : CopyCondition.GOOD)
                    .availabilityStatus(CopyStatus.AVAILABLE)
                    .acquiredDate(LocalDate.now())
                    .remarks("Added via inventory replenishment")
                    .build();
            newCopies.add(copy);
        }

        return bookCopyRepository.saveAll(newCopies);
    }

    @Override
    public Book updateStatus(Long id, BookStatus status) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));
        book.setStatus(status);
        return bookRepository.save(book);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Book> findById(Long id) {
        return bookRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Book> findByIsbn(String isbn) {
        return bookRepository.findByIsbn(isbn.replaceAll("[\\s-]", ""));
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Book> searchBooks(String keyword, Long categoryId, Long authorId, Long publisherId,
                                  String language, BookStatus status, Boolean availableOnly, Pageable pageable) {
        Specification<Book> spec = BookSpecification.filter(
                keyword, categoryId, authorId, publisherId, language, status, availableOnly
        );
        return bookRepository.findAll(spec, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public long countTotalBooks() {
        return bookRepository.count();
    }

    @Override
    @Transactional(readOnly = true)
    public long countAvailableBooks() {
        return bookCopyRepository.countByAvailabilityStatus(CopyStatus.AVAILABLE);
    }

    @Override
    public void deleteBook(Long id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));
        bookRepository.delete(book);
    }
}
