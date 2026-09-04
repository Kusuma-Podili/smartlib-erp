package com.library.erp.service;

import com.library.erp.dto.catalog.CategoryDto;
import com.library.erp.entity.Category;

import java.util.List;
import java.util.Optional;

public interface CategoryService {
    Category createCategory(CategoryDto dto);
    Category updateCategory(Long id, CategoryDto dto);
    Optional<Category> findById(Long id);
    Optional<Category> findByCode(String code);
    List<Category> findAllCategories();
    List<Category> findRootCategories();
    void deleteCategory(Long id);
    long countCategories();
}
