package com.library.erp.controller.librarian;

import com.library.erp.dto.circulation.FinePaymentDto;
import com.library.erp.entity.*;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.LibrarianRepository;
import com.library.erp.service.AuthService;
import com.library.erp.service.FineService;
import com.library.erp.service.MemberService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.Collections;
import java.util.List;

@Controller
@RequestMapping("/librarian/fines")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianFineController {

    private final FineService fineService;
    private final MemberService memberService;
    private final AuthService authService;
    private final LibrarianRepository librarianRepository;

    @GetMapping
    public String cashierDesk(@RequestParam(value = "memberCode", required = false) String memberCode, Model model) {
        List<Fine> unpaidFines = Collections.emptyList();
        Member member = null;

        if (memberCode != null && !memberCode.isBlank()) {
            member = memberService.findByMemberCode(memberCode.trim()).orElse(null);
            if (member != null) {
                unpaidFines = fineService.findUnpaidFinesByMember(member.getId());
                model.addAttribute("outstandingBalance", fineService.getOutstandingBalanceForMember(member.getId()));
            } else {
                model.addAttribute("errorMessage", "Member not found with code: " + memberCode);
            }
        }

        model.addAttribute("member", member);
        model.addAttribute("unpaidFines", unpaidFines);
        model.addAttribute("memberCode", memberCode);
        model.addAttribute("activeMenu", "lib-fines");
        return "librarian/circulation/fines";
    }

    @PostMapping("/pay")
    public String collectFine(@Valid @ModelAttribute("paymentDto") FinePaymentDto dto,
                              BindingResult bindingResult,
                              @RequestParam("memberCode") String memberCode,
                              RedirectAttributes redirectAttributes) {
        if (bindingResult.hasErrors()) {
            redirectAttributes.addFlashAttribute("errorMessage", "Invalid payment parameters provided.");
            return "redirect:/librarian/fines?memberCode=" + memberCode;
        }

        try {
            User currentUser = authService.getCurrentAuthenticatedUser();
            Librarian librarian = librarianRepository.findByUserId(currentUser.getId()).orElse(null);

            FinePayment payment = fineService.recordPayment(dto, librarian);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Payment of ₹" + payment.getAmountPaid() + " recorded successfully. Issued Receipt: " + payment.getReceiptNumber());

        } catch (BusinessRuleViolationException | ResourceNotFoundException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
        }

        return "redirect:/librarian/fines?memberCode=" + memberCode;
    }

    @PostMapping("/{id}/waive")
    public String waiveFine(@PathVariable("id") Long fineId,
                            @RequestParam("memberCode") String memberCode,
                            @RequestParam(value = "reason", defaultValue = "Authorized courtesy waiver") String reason,
                            RedirectAttributes redirectAttributes) {
        fineService.waiveFine(fineId, reason);
        redirectAttributes.addFlashAttribute("successMessage", "Fine #" + fineId + " has been waived.");
        return "redirect:/librarian/fines?memberCode=" + memberCode;
    }
}
