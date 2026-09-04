package com.library.erp.entity;

import com.library.erp.entity.enums.BookStatus;
import com.library.erp.entity.enums.CopyStatus;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "books", indexes = {
        @Index(name = "idx_book_isbn", columnList = "isbn"),
        @Index(name = "idx_book_title", columnList = "title")
})
public class Book extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "isbn", nullable = false, unique = true, length = 20)
    private String isbn;

    @Column(name = "title", nullable = false, length = 200)
    private String title;

    @Column(name = "subtitle", length = 255)
    private String subtitle;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "category_id")
    private Category category;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "publisher_id")
    private Publisher publisher;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(
            name = "book_authors",
            joinColumns = @JoinColumn(name = "book_id"),
            inverseJoinColumns = @JoinColumn(name = "author_id")
    )
    @Builder.Default
    private Set<Author> authors = new HashSet<>();

    @Column(name = "edition", length = 50)
    private String edition;

    @Column(name = "publication_year")
    private Integer publicationYear;

    @Column(name = "language", length = 50)
    @Builder.Default
    private String language = "English";

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "cover_image_url", length = 255)
    private String coverImageUrl;

    @Column(name = "shelf_number", length = 50)
    private String shelfNumber;

    @Column(name = "rack_number", length = 50)
    private String rackNumber;

    @Column(name = "price", precision = 10, scale = 2)
    private BigDecimal price;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    @Builder.Default
    private BookStatus status = BookStatus.ACTIVE;

    @OneToMany(mappedBy = "book", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<BookCopy> copies = new ArrayList<>();

    public String getAuthorsFormatted() {
        if (authors == null || authors.isEmpty()) return "Unknown Author";
        return authors.stream().map(Author::getFullName).collect(Collectors.joining(", "));
    }

    public int getTotalCopiesCount() {
        return copies != null ? copies.size() : 0;
    }

    public long getAvailableCopiesCount() {
        if (copies == null) return 0;
        return copies.stream().filter(c -> c.getAvailabilityStatus() == CopyStatus.AVAILABLE).count();
    }

    public long getIssuedCopiesCount() {
        if (copies == null) return 0;
        return copies.stream().filter(c -> c.getAvailabilityStatus() == CopyStatus.BORROWED).count();
    }

    public long getReservedCopiesCount() {
        if (copies == null) return 0;
        return copies.stream().filter(c -> c.getAvailabilityStatus() == CopyStatus.RESERVED).count();
    }

    public long getLostCopiesCount() {
        if (copies == null) return 0;
        return copies.stream().filter(c -> c.getAvailabilityStatus() == CopyStatus.LOST).count();
    }

    public long getDamagedCopiesCount() {
        if (copies == null) return 0;
        return copies.stream().filter(c -> c.getAvailabilityStatus() == CopyStatus.MAINTENANCE).count();
    }
}
