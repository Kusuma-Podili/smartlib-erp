package com.library.erp.dto.catalog;

import jakarta.validation.constraints.*;
import lombok.*;

import java.math.BigDecimal;
import java.util.HashSet;
import java.util.Set;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BookRequestDto {

    private Long id;

    @NotBlank(message = "ISBN is mandatory")
    @Pattern(regexp = "^(97(8|9))?\\d{9}(\\d|X)$|^[0-9-]{10,17}$", message = "Invalid ISBN format")
    private String isbn;

    @NotBlank(message = "Book title is mandatory")
    @Size(max = 200, message = "Title cannot exceed 200 characters")
    private String title;

    private String subtitle;

    @NotNull(message = "Please select a category")
    private Long categoryId;

    @NotNull(message = "Please select a publisher")
    private Long publisherId;

    @NotEmpty(message = "At least one author must be specified")
    @Builder.Default
    private Set<Long> authorIds = new HashSet<>();

    private String edition;

    @Min(value = 1000, message = "Year must be valid")
    @Max(value = 2100, message = "Year must be realistic")
    private Integer publicationYear;

    private String language;

    private String description;

    private String coverImageUrl;

    private String shelfNumber;

    private String rackNumber;

    @PositiveOrZero(message = "Price must be non-negative")
    private BigDecimal price;

    @Min(value = 1, message = "Initial copies count must be at least 1")
    @Builder.Default
    private Integer initialCopies = 1;
}
