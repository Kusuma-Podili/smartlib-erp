package com.library.erp.controller.admin;

import com.library.erp.dto.catalog.CategoryDto;
import com.library.erp.entity.Category;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.service.CategoryService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/admin/categories")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminCategoryController {

    private final CategoryService categoryService;

    @GetMapping
    public String listCategories(Model model) {
        model.addAttribute("categories", categoryService.findAllCategories());
        if (!model.containsAttribute("categoryDto")) {
            model.addAttribute("categoryDto", new CategoryDto());
        }
        model.addAttribute("activeMenu", "admin-categories");
        return "admin/categories/list";
    }

    @PostMapping
    public String createCategory(@Valid @ModelAttribute("categoryDto") CategoryDto categoryDto,
                                 BindingResult bindingResult,
                                 RedirectAttributes redirectAttributes,
                                 Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("categories", categoryService.findAllCategories());
            model.addAttribute("activeMenu", "admin-categories");
            return "admin/categories/list";
        }

        try {
            Category created = categoryService.createCategory(categoryDto);
            redirectAttributes.addFlashAttribute("successMessage", "Category '" + created.getName() + "' created successfully.");
            return "redirect:/admin/categories";
        } catch (DuplicateResourceException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
            return "redirect:/admin/categories";
        }
    }
}
