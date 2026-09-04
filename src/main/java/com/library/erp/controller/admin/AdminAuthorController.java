package com.library.erp.controller.admin;

import com.library.erp.dto.catalog.AuthorDto;
import com.library.erp.entity.Author;
import com.library.erp.service.AuthorService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/admin/authors")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminAuthorController {

    private final AuthorService authorService;

    @GetMapping
    public String listAuthors(Model model) {
        model.addAttribute("authors", authorService.findAllAuthors());
        if (!model.containsAttribute("authorDto")) {
            model.addAttribute("authorDto", new AuthorDto());
        }
        model.addAttribute("activeMenu", "admin-authors");
        return "admin/authors/list";
    }

    @PostMapping
    public String createAuthor(@Valid @ModelAttribute("authorDto") AuthorDto authorDto,
                               BindingResult bindingResult,
                               RedirectAttributes redirectAttributes,
                               Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("authors", authorService.findAllAuthors());
            model.addAttribute("activeMenu", "admin-authors");
            return "admin/authors/list";
        }

        Author created = authorService.createAuthor(authorDto);
        redirectAttributes.addFlashAttribute("successMessage", "Author '" + created.getFullName() + "' created successfully.");
        return "redirect:/admin/authors";
    }
}
