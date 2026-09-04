package com.library.erp.service.impl;

import com.library.erp.dto.catalog.CategoryDto;
import com.library.erp.entity.Category;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.CategoryRepository;
import com.library.erp.service.CategoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class CategoryServiceImpl implements CategoryService {

    private final CategoryRepository categoryRepository;

    @Override
    public Category createCategory(CategoryDto dto) {
        if (categoryRepository.existsByCode(dto.getCode().trim().toUpperCase())) {
            throw new DuplicateResourceException("Category with code '" + dto.getCode() + "' already exists.");
        }
        if (categoryRepository.existsByName(dto.getName().trim())) {
            throw new DuplicateResourceException("Category with name '" + dto.getName() + "' already exists.");
        }

        Category parent = null;
        if (dto.getParentCategoryId() != null) {
            parent = categoryRepository.findById(dto.getParentCategoryId())
                    .orElseThrow(() -> new ResourceNotFoundException("Parent Category not found with id: " + dto.getParentCategoryId()));
        }

        Category category = Category.builder()
                .name(dto.getName().trim())
                .code(dto.getCode().trim().toUpperCase())
                .description(dto.getDescription())
                .parentCategory(parent)
                .build();

        return categoryRepository.save(category);
    }

    @Override
    public Category updateCategory(Long id, CategoryDto dto) {
        Category category = categoryRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Category not found with id: " + id));

        category.setName(dto.getName().trim());
        category.setDescription(dto.getDescription());

        if (dto.getParentCategoryId() != null) {
            Category parent = categoryRepository.findById(dto.getParentCategoryId())
                    .orElseThrow(() -> new ResourceNotFoundException("Parent category not found"));
            category.setParentCategory(parent);
        } else {
            category.setParentCategory(null);
        }

        return categoryRepository.save(category);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Category> findById(Long id) {
        return categoryRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Category> findByCode(String code) {
        return categoryRepository.findByCode(code);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Category> findAllCategories() {
        return categoryRepository.findByOrderByNameAsc();
    }

    @Override
    @Transactional(readOnly = true)
    public List<Category> findRootCategories() {
        return categoryRepository.findByParentCategoryIsNullOrderByNameAsc();
    }

    @Override
    public void deleteCategory(Long id) {
        if (!categoryRepository.existsById(id)) {
            throw new ResourceNotFoundException("Category not found with id: " + id);
        }
        categoryRepository.deleteById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public long countCategories() {
        return categoryRepository.count();
    }
}
