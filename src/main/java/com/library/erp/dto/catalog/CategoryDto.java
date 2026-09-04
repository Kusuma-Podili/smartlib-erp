package com.library.erp.dto.catalog;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CategoryDto {
    private Long id;

    @NotBlank(message = "Category name is required")
    private String name;

    @NotBlank(message = "Category code is required (e.g. CS, LIT, SCI)")
    private String code;

    private String description;

    private Long parentCategoryId;
    private String parentCategoryName;
    private int bookCount;
}
