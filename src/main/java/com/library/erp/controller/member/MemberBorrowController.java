package com.library.erp.controller.member;

import com.library.erp.entity.BorrowRecord;
import com.library.erp.entity.Member;
import com.library.erp.entity.User;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.AuthService;
import com.library.erp.service.BorrowService;
import com.library.erp.service.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.Collections;
import java.util.List;

@Controller
@RequestMapping("/member/loans")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberBorrowController {

    private final BorrowService borrowService;
    private final MemberService memberService;
    private final AuthService authService;

    @GetMapping
    public String myLoans(@RequestParam(value = "page", defaultValue = "0") int page,
                          @RequestParam(value = "size", defaultValue = "10") int size,
                          Model model) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        Member member = memberService.findByUserId(currentUser.getId()).orElse(null);

        List<BorrowRecord> activeLoans = Collections.emptyList();
        Page<BorrowRecord> history = Page.empty();

        if (member != null) {
            activeLoans = borrowService.findActiveLoansByMember(member.getId());
            history = borrowService.findLoanHistoryByMember(member.getId(), PageRequest.of(page, size));
        }

        model.addAttribute("activeLoans", activeLoans);
        model.addAttribute("history", history.getContent());
        model.addAttribute("totalPages", history.getTotalPages());
        model.addAttribute("currentPage", page);
        model.addAttribute("activeMenu", "mem-loans");

        return "member/circulation/loans";
    }

    @PostMapping("/{id}/renew")
    public String requestRenewal(@PathVariable("id") Long borrowRecordId, RedirectAttributes redirectAttributes) {
        try {
            User currentUser = authService.getCurrentAuthenticatedUser();
            Member member = memberService.findByUserId(currentUser.getId())
                    .orElseThrow(() -> new ResourceNotFoundException("Member profile not found."));

            BorrowRecord record = borrowService.findById(borrowRecordId)
                    .orElseThrow(() -> new ResourceNotFoundException("Loan record not found."));

            if (!record.getMember().getId().equals(member.getId())) {
                throw new BusinessRuleViolationException("You cannot renew another patron's book loan.");
            }

            BorrowRecord renewed = borrowService.renewLoan(borrowRecordId);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Loan renewed successfully! Your new due date is " + renewed.getDueDate());
        } catch (BusinessRuleViolationException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
        }

        return "redirect:/member/loans";
    }
}
