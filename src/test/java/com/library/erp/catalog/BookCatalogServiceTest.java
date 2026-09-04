package com.library.erp.catalog;

import com.library.erp.dto.catalog.AuthorDto;
import com.library.erp.dto.catalog.BookRequestDto;
import com.library.erp.dto.catalog.CategoryDto;
import com.library.erp.dto.catalog.PublisherDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.entity.enums.CopyStatus;
import com.library.erp.service.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class BookCatalogServiceTest {

    @Autowired
    private BookService bookService;

    @Autowired
    private BookCopyService bookCopyService;

    @Autowired
    private CategoryService categoryService;

    @Autowired
    private AuthorService authorService;

    @Autowired
    private PublisherService publisherService;

    private Category testCategory;
    private Publisher testPublisher;
    private Author testAuthor;

    @BeforeEach
    void setUp() {
        testCategory = categoryService.createCategory(CategoryDto.builder()
                .name("Computer Science " + System.currentTimeMillis())
                .code("CS_" + System.currentTimeMillis())
                .description("Computing literature")
                .build());

        testPublisher = publisherService.createPublisher(PublisherDto.builder()
                .name("Pearson Tech " + System.currentTimeMillis())
                .contactEmail("contact@pearson.test")
                .build());

        testAuthor = authorService.createAuthor(AuthorDto.builder()
                .firstName("Joshua")
                .lastName("Bloch")
                .email("joshua@bloch.test")
                .build());
    }

    @Test
    @DisplayName("Test 1: Catalog new book creates logical title and provisioned physical copies with unique barcodes")
    void createBookShouldGeneratePhysicalCopiesWithBarcodes() {
        String isbn = "978" + (System.currentTimeMillis() % 10000000000L);
        BookRequestDto dto = BookRequestDto.builder()
                .isbn(isbn)
                .title("Effective Java 3rd Edition")
                .subtitle("Best practices for the Java platform")
                .categoryId(testCategory.getId())
                .publisherId(testPublisher.getId())
                .authorIds(Set.of(testAuthor.getId()))
                .edition("3rd")
                .publicationYear(2018)
                .language("English")
                .price(BigDecimal.valueOf(799.00))
                .shelfNumber("S-04")
                .rackNumber("R-12")
                .initialCopies(3)
                .build();

        Book savedBook = bookService.createBook(dto);

        assertThat(savedBook.getId()).isNotNull();
        assertThat(savedBook.getTitle()).isEqualTo("Effective Java 3rd Edition");
        assertThat(savedBook.getAuthorsFormatted()).contains("Joshua Bloch");

        List<BookCopy> copies = bookCopyService.findCopiesByBookId(savedBook.getId());
        assertThat(copies).hasSize(3);
        assertThat(copies.get(0).getBarcode()).contains(isbn);
        assertThat(copies.get(0).getAvailabilityStatus()).isEqualTo(CopyStatus.AVAILABLE);
        assertThat(savedBook.getAvailableCopiesCount()).isEqualTo(3);
    }

    @Test
    @DisplayName("Test 2: Replenishing copies generates subsequent copy numbers and increases available inventory")
    void addCopiesShouldIncrementStartingNumber() {
        String isbn = "978" + (System.currentTimeMillis() % 10000000000L);
        BookRequestDto dto = BookRequestDto.builder()
                .isbn(isbn)
                .title("Design Patterns")
                .categoryId(testCategory.getId())
                .publisherId(testPublisher.getId())
                .authorIds(Set.of(testAuthor.getId()))
                .initialCopies(2)
                .build();

        Book savedBook = bookService.createBook(dto);
        assertThat(bookCopyService.findCopiesByBookId(savedBook.getId())).hasSize(2);

        // Add 2 more copies
        List<BookCopy> added = bookService.addCopies(savedBook.getId(), 2, CopyCondition.NEW);
        assertThat(added).hasSize(2);
        assertThat(added.get(0).getCopyNumber()).isEqualTo(3);
        assertThat(added.get(1).getCopyNumber()).isEqualTo(4);

        List<BookCopy> allCopies = bookCopyService.findCopiesByBookId(savedBook.getId());
        assertThat(allCopies).hasSize(4);
    }

    @Test
    @DisplayName("Test 3: Marking a physical copy as lost removes it from available pool")
    void markCopyAsLostShouldUpdateAvailability() {
        String isbn = "978" + (System.currentTimeMillis() % 10000000000L);
        BookRequestDto dto = BookRequestDto.builder()
                .isbn(isbn)
                .title("Refactoring")
                .categoryId(testCategory.getId())
                .publisherId(testPublisher.getId())
                .authorIds(Set.of(testAuthor.getId()))
                .initialCopies(2)
                .build();

        Book savedBook = bookService.createBook(dto);
        List<BookCopy> copies = bookCopyService.findCopiesByBookId(savedBook.getId());
        BookCopy firstCopy = copies.get(0);

        bookCopyService.markAsLost(firstCopy.getId(), "Reported missing during shelf audit");

        BookCopy updatedCopy = bookCopyService.findById(firstCopy.getId()).orElseThrow();
        assertThat(updatedCopy.getAvailabilityStatus()).isEqualTo(CopyStatus.LOST);
        assertThat(updatedCopy.getConditionStatus()).isEqualTo(CopyCondition.LOST);

        List<BookCopy> availableCopies = bookCopyService.findAvailableCopiesByBookId(savedBook.getId());
        assertThat(availableCopies).hasSize(1);
    }

    @Test
    @DisplayName("Test 4: Catalog multi-predicate specification search filters by keyword and category")
    void searchSpecificationFiltersCorrectly() {
        String uniqueTitle = "Domain Driven Design Special " + System.currentTimeMillis();
        String isbn = "978" + (System.currentTimeMillis() % 10000000000L);
        BookRequestDto dto = BookRequestDto.builder()
                .isbn(isbn)
                .title(uniqueTitle)
                .categoryId(testCategory.getId())
                .publisherId(testPublisher.getId())
                .authorIds(Set.of(testAuthor.getId()))
                .initialCopies(1)
                .build();
        bookService.createBook(dto);

        Page<Book> result = bookService.searchBooks(
                "Domain Driven", testCategory.getId(), null, null, null, null, null,
                PageRequest.of(0, 10)
        );

        assertThat(result.getContent()).isNotEmpty();
        assertThat(result.getContent().get(0).getTitle()).isEqualTo(uniqueTitle);
    }
}
