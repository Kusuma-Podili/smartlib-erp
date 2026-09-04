package com.library.erp.controller.librarian;

import com.library.erp.dto.circulation.BorrowRequestDto;
import com.library.erp.entity.BorrowRecord;
import com.library.erp.entity.Librarian;
import com.library.erp.entity.User;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.LibrarianRepository;
import com.library.erp.service.AuthService;
import com.library.erp.service.BorrowService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/librarian/borrow")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianBorrowController {

    private final BorrowService borrowService;
    private final AuthService authService;
    private final LibrarianRepository librarianRepository;

    @GetMapping
    public String borrowForm(@RequestParam(value = "memberCode", required = false) String memberCode,
                             @RequestParam(value = "barcode", required = false) String barcode,
                             Model model) {
        BorrowRequestDto dto = BorrowRequestDto.builder()
                .memberCode(memberCode)
                .barcode(barcode)
                .build();

        model.addAttribute("borrowDto", dto);
        model.addAttribute("activeMenu", "lib-borrow");
        return "librarian/circulation/borrow";
    }

    @PostMapping
    public String issueBook(@Valid @ModelAttribute("borrowDto") BorrowRequestDto dto,
                            BindingResult bindingResult,
                            RedirectAttributes redirectAttributes,
                            Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("activeMenu", "lib-borrow");
            return "librarian/circulation/borrow";
        }

        try {
            User currentUser = authService.getCurrentAuthenticatedUser();
            Librarian librarian = librarianRepository.findByUserId(currentUser.getId()).orElse(null);

            BorrowRecord record = borrowService.issueBook(dto, librarian);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Successfully issued copy " + record.getBookCopy().getBarcode() +
                    " ('" + record.getBookCopy().getBook().getTitle() + "') to " +
                    record.getMember().getUser().getFullName() + ". Due date: " + record.getDueDate());

            return "redirect:/librarian/borrow";
        } catch (BusinessRuleViolationException | ResourceNotFoundException e) {
            model.addAttribute("errorMessage", e.getMessage());
            model.addAttribute("activeMenu", "lib-borrow");
            return "librarian/circulation/borrow";
        }
    }

    @PostMapping("/{id}/renew")
    public String renewLoan(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        try {
            BorrowRecord renewed = borrowService.renewLoan(id);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Loan renewed successfully. New due date is " + renewed.getDueDate());
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
        }
        return "redirect:/librarian/dashboard";
    }
}
