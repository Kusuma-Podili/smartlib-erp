package com.library.erp.controller.librarian;

import com.library.erp.dto.circulation.ReturnProcessDto;
import com.library.erp.entity.Librarian;
import com.library.erp.entity.ReturnRecord;
import com.library.erp.entity.User;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.LibrarianRepository;
import com.library.erp.service.AuthService;
import com.library.erp.service.ReturnService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.math.BigDecimal;

@Controller
@RequestMapping("/librarian/return")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianReturnController {

    private final ReturnService returnService;
    private final AuthService authService;
    private final LibrarianRepository librarianRepository;

    @GetMapping
    public String returnForm(@RequestParam(value = "barcode", required = false) String barcode, Model model) {
        ReturnProcessDto dto = ReturnProcessDto.builder().barcode(barcode).build();
        model.addAttribute("returnDto", dto);
        model.addAttribute("activeMenu", "lib-return");
        return "librarian/circulation/return";
    }

    @PostMapping
    public String processReturn(@Valid @ModelAttribute("returnDto") ReturnProcessDto dto,
                                BindingResult bindingResult,
                                RedirectAttributes redirectAttributes,
                                Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("activeMenu", "lib-return");
            return "librarian/circulation/return";
        }

        try {
            User currentUser = authService.getCurrentAuthenticatedUser();
            Librarian librarian = librarianRepository.findByUserId(currentUser.getId()).orElse(null);

            ReturnRecord returnRecord = returnService.processReturn(dto, librarian);

            String message = "Book '" + returnRecord.getBorrowRecord().getBookCopy().getBook().getTitle() +
                             "' (Copy " + returnRecord.getBorrowRecord().getBookCopy().getBarcode() + ") successfully checked in.";

            if (returnRecord.getFineAssessed().compareTo(BigDecimal.ZERO) > 0) {
                message += " [Notice: Late / damage fine of ₹" + returnRecord.getFineAssessed() +
                           " was generated for " + returnRecord.getBorrowRecord().getMember().getUser().getFullName() + "].";
            }

            redirectAttributes.addFlashAttribute("successMessage", message);
            return "redirect:/librarian/return";
        } catch (ResourceNotFoundException e) {
            model.addAttribute("errorMessage", e.getMessage());
            model.addAttribute("activeMenu", "lib-return");
            return "librarian/circulation/return";
        }
    }
}
