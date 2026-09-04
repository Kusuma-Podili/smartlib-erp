package com.library.erp.controller.admin;

import com.library.erp.dto.catalog.BookRequestDto;
import com.library.erp.entity.Author;
import com.library.erp.entity.Book;
import com.library.erp.entity.enums.BookStatus;
import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.*;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.stream.Collectors;

@Slf4j
@Controller
@RequestMapping("/admin/books")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminBookController {

    private final BookService bookService;
    private final BookCopyService bookCopyService;
    private final CategoryService categoryService;
    private final AuthorService authorService;
    private final PublisherService publisherService;

    @GetMapping
    public String listBooks(@RequestParam(value = "keyword", required = false) String keyword,
                            @RequestParam(value = "categoryId", required = false) Long categoryId,
                            @RequestParam(value = "authorId", required = false) Long authorId,
                            @RequestParam(value = "status", required = false) BookStatus status,
                            @RequestParam(value = "page", defaultValue = "0") int page,
                            @RequestParam(value = "size", defaultValue = "10") int size,
                            Model model) {
        Page<Book> bookPage = bookService.searchBooks(
                keyword, categoryId, authorId, null, null, status, false,
                PageRequest.of(page, size, Sort.by("id").descending())
        );

        model.addAttribute("books", bookPage.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", bookPage.getTotalPages());
        model.addAttribute("totalElements", bookPage.getTotalElements());
        model.addAttribute("keyword", keyword);
        model.addAttribute("categoryId", categoryId);
        model.addAttribute("authorId", authorId);
        model.addAttribute("selectedStatus", status);
        model.addAttribute("categories", categoryService.findAllCategories());
        model.addAttribute("authors", authorService.findAllAuthors());
        model.addAttribute("activeMenu", "admin-books");

        return "admin/books/list";
    }

    @GetMapping("/new")
    public String newBookForm(Model model) {
        if (!model.containsAttribute("bookDto")) {
            model.addAttribute("bookDto", new BookRequestDto());
        }
        populateCatalogFormModel(model);
        model.addAttribute("activeMenu", "admin-books");
        return "admin/books/form";
    }

    @PostMapping
    public String saveBook(@Valid @ModelAttribute("bookDto") BookRequestDto bookDto,
                           BindingResult bindingResult,
                           RedirectAttributes redirectAttributes,
                           Model model) {
        if (bindingResult.hasErrors()) {
            populateCatalogFormModel(model);
            return "admin/books/form";
        }

        try {
            Book saved = bookService.createBook(bookDto);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Book '" + saved.getTitle() + "' was cataloged successfully with " + saved.getTotalCopiesCount() + " physical copies.");
            return "redirect:/admin/books/" + saved.getId();
        } catch (DuplicateResourceException e) {
            model.addAttribute("errorMessage", e.getMessage());
            populateCatalogFormModel(model);
            return "admin/books/form";
        }
    }

    @GetMapping("/{id}")
    public String viewBook(@PathVariable("id") Long id, Model model) {
        Book book = bookService.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));

        model.addAttribute("book", book);
        model.addAttribute("copies", bookCopyService.findCopiesByBookId(id));
        model.addAttribute("activeMenu", "admin-books");
        return "admin/books/view";
    }

    @GetMapping("/{id}/edit")
    public String editBookForm(@PathVariable("id") Long id, Model model) {
        Book book = bookService.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));

        BookRequestDto dto = BookRequestDto.builder()
                .id(book.getId())
                .isbn(book.getIsbn())
                .title(book.getTitle())
                .subtitle(book.getSubtitle())
                .categoryId(book.getCategory().getId())
                .publisherId(book.getPublisher().getId())
                .authorIds(book.getAuthors().stream().map(Author::getId).collect(Collectors.toSet()))
                .edition(book.getEdition())
                .publicationYear(book.getPublicationYear())
                .language(book.getLanguage())
                .description(book.getDescription())
                .shelfNumber(book.getShelfNumber())
                .rackNumber(book.getRackNumber())
                .price(book.getPrice())
                .build();

        model.addAttribute("bookDto", dto);
        populateCatalogFormModel(model);
        model.addAttribute("isEdit", true);
        model.addAttribute("activeMenu", "admin-books");
        return "admin/books/form";
    }

    @PostMapping("/{id}/edit")
    public String updateBook(@PathVariable("id") Long id,
                             @Valid @ModelAttribute("bookDto") BookRequestDto bookDto,
                             BindingResult bindingResult,
                             RedirectAttributes redirectAttributes,
                             Model model) {
        if (bindingResult.hasErrors()) {
            populateCatalogFormModel(model);
            model.addAttribute("isEdit", true);
            return "admin/books/form";
        }

        try {
            bookService.updateBook(id, bookDto);
            redirectAttributes.addFlashAttribute("successMessage", "Book updated successfully.");
            return "redirect:/admin/books/" + id;
        } catch (Exception e) {
            model.addAttribute("errorMessage", e.getMessage());
            populateCatalogFormModel(model);
            model.addAttribute("isEdit", true);
            return "admin/books/form";
        }
    }

    @PostMapping("/{id}/copies/add")
    public String addCopies(@PathVariable("id") Long id,
                            @RequestParam("copyCount") int copyCount,
                            @RequestParam(value = "condition", defaultValue = "NEW") CopyCondition condition,
                            RedirectAttributes redirectAttributes) {
        if (copyCount < 1 || copyCount > 50) {
            redirectAttributes.addFlashAttribute("errorMessage", "Number of copies must be between 1 and 50.");
            return "redirect:/admin/books/" + id;
        }

        bookService.addCopies(id, copyCount, condition);
        redirectAttributes.addFlashAttribute("successMessage", "Added " + copyCount + " new copies to inventory.");
        return "redirect:/admin/books/" + id;
    }

    @PostMapping("/{id}/status")
    public String toggleStatus(@PathVariable("id") Long id,
                               @RequestParam("status") BookStatus status,
                               RedirectAttributes redirectAttributes) {
        bookService.updateStatus(id, status);
        redirectAttributes.addFlashAttribute("successMessage", "Book status updated to " + status);
        return "redirect:/admin/books/" + id;
    }

    private void populateCatalogFormModel(Model model) {
        model.addAttribute("categories", categoryService.findAllCategories());
        model.addAttribute("publishers", publisherService.findAllPublishers());
        model.addAttribute("authors", authorService.findAllAuthors());
    }
}
