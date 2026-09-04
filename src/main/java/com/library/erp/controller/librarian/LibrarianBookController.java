package com.library.erp.controller.librarian;

import com.library.erp.dto.catalog.BookRequestDto;
import com.library.erp.entity.Book;
import com.library.erp.entity.BookCopy;
import com.library.erp.entity.enums.BookStatus;
import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.*;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/librarian/books")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianBookController {

    private final BookService bookService;
    private final BookCopyService bookCopyService;
    private final CategoryService categoryService;
    private final AuthorService authorService;
    private final PublisherService publisherService;

    @GetMapping
    public String searchCatalog(@RequestParam(value = "keyword", required = false) String keyword,
                                @RequestParam(value = "categoryId", required = false) Long categoryId,
                                @RequestParam(value = "page", defaultValue = "0") int page,
                                @RequestParam(value = "size", defaultValue = "10") int size,
                                Model model) {
        Page<Book> bookPage = bookService.searchBooks(
                keyword, categoryId, null, null, null, BookStatus.ACTIVE, false,
                PageRequest.of(page, size, Sort.by("title").ascending())
        );

        model.addAttribute("books", bookPage.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", bookPage.getTotalPages());
        model.addAttribute("keyword", keyword);
        model.addAttribute("categoryId", categoryId);
        model.addAttribute("categories", categoryService.findAllCategories());
        model.addAttribute("activeMenu", "lib-books");

        return "librarian/books/list";
    }

    @GetMapping("/new")
    public String newBookForm(Model model) {
        if (!model.containsAttribute("bookDto")) {
            model.addAttribute("bookDto", new BookRequestDto());
        }
        model.addAttribute("categories", categoryService.findAllCategories());
        model.addAttribute("publishers", publisherService.findAllPublishers());
        model.addAttribute("authors", authorService.findAllAuthors());
        model.addAttribute("activeMenu", "lib-books");
        return "librarian/books/form";
    }

    @PostMapping
    public String saveBook(@Valid @ModelAttribute("bookDto") BookRequestDto bookDto,
                           BindingResult bindingResult,
                           RedirectAttributes redirectAttributes,
                           Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("categories", categoryService.findAllCategories());
            model.addAttribute("publishers", publisherService.findAllPublishers());
            model.addAttribute("authors", authorService.findAllAuthors());
            model.addAttribute("activeMenu", "lib-books");
            return "librarian/books/form";
        }

        Book saved = bookService.createBook(bookDto);
        redirectAttributes.addFlashAttribute("successMessage", "Book '" + saved.getTitle() + "' added successfully with " + saved.getTotalCopiesCount() + " copies.");
        return "redirect:/librarian/books/" + saved.getId();
    }

    @GetMapping("/{id}")
    public String viewBookDetails(@PathVariable("id") Long id, Model model) {
        Book book = bookService.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + id));

        model.addAttribute("book", book);
        model.addAttribute("copies", bookCopyService.findCopiesByBookId(id));
        model.addAttribute("activeMenu", "lib-books");
        return "librarian/books/view";
    }

    @PostMapping("/{id}/copies/add")
    public String addCopies(@PathVariable("id") Long id,
                            @RequestParam("copyCount") int copyCount,
                            RedirectAttributes redirectAttributes) {
        bookService.addCopies(id, copyCount, CopyCondition.NEW);
        redirectAttributes.addFlashAttribute("successMessage", "Added " + copyCount + " new copies to inventory.");
        return "redirect:/librarian/books/" + id;
    }

    @PostMapping("/copies/{copyId}/mark-lost")
    public String markLost(@PathVariable("copyId") Long copyId,
                           @RequestParam("bookId") Long bookId,
                           @RequestParam(value = "remarks", required = false) String remarks,
                           RedirectAttributes redirectAttributes) {
        bookCopyService.markAsLost(copyId, remarks);
        redirectAttributes.addFlashAttribute("successMessage", "Copy marked as LOST.");
        return "redirect:/librarian/books/" + bookId;
    }

    @PostMapping("/copies/{copyId}/mark-damaged")
    public String markDamaged(@PathVariable("copyId") Long copyId,
                             @RequestParam("bookId") Long bookId,
                             @RequestParam(value = "remarks", required = false) String remarks,
                             RedirectAttributes redirectAttributes) {
        bookCopyService.markAsDamaged(copyId, remarks);
        redirectAttributes.addFlashAttribute("successMessage", "Copy marked as DAMAGED and moved to maintenance.");
        return "redirect:/librarian/books/" + bookId;
    }
}
