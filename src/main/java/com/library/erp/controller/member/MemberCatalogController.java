package com.library.erp.controller.member;

import com.library.erp.entity.Book;
import com.library.erp.entity.Member;
import com.library.erp.entity.User;
import com.library.erp.entity.enums.BookStatus;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.*;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/member/catalog")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberCatalogController {

    private final BookService bookService;
    private final CategoryService categoryService;
    private final ReservationService reservationService;
    private final MemberService memberService;
    private final AuthService authService;

    @GetMapping
    public String browseCatalog(@RequestParam(value = "keyword", required = false) String keyword,
                                @RequestParam(value = "categoryId", required = false) Long categoryId,
                                @RequestParam(value = "availableOnly", required = false) Boolean availableOnly,
                                @RequestParam(value = "page", defaultValue = "0") int page,
                                @RequestParam(value = "size", defaultValue = "12") int size,
                                Model model) {
        Page<Book> books = bookService.searchBooks(
                keyword, categoryId, null, null, null, BookStatus.ACTIVE, availableOnly,
                PageRequest.of(page, size, Sort.by("title").ascending())
        );

        model.addAttribute("books", books.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", books.getTotalPages());
        model.addAttribute("keyword", keyword);
        model.addAttribute("categoryId", categoryId);
        model.addAttribute("availableOnly", availableOnly);
        model.addAttribute("categories", categoryService.findAllCategories());
        model.addAttribute("activeMenu", "mem-catalog");

        return "member/catalog/index";
    }

    @PostMapping("/{id}/reserve")
    public String reserveBook(@PathVariable("id") Long bookId,
                             @RequestParam(value = "remarks", required = false) String remarks,
                             RedirectAttributes redirectAttributes) {
        try {
            User currentUser = authService.getCurrentAuthenticatedUser();
            Member member = memberService.findByUserId(currentUser.getId())
                    .orElseThrow(() -> new ResourceNotFoundException("Member record not found for user."));

            reservationService.reserveBook(member.getId(), bookId, remarks);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Reservation placed successfully! You have been added to the hold queue.");
        } catch (BusinessRuleViolationException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
        }

        return "redirect:/member/reservations";
    }
}
