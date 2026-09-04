package com.library.erp.controller.member;

import com.library.erp.entity.Fine;
import com.library.erp.entity.FinePayment;
import com.library.erp.entity.Member;
import com.library.erp.entity.User;
import com.library.erp.service.AuthService;
import com.library.erp.service.FineService;
import com.library.erp.service.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.math.BigDecimal;

@Controller
@RequestMapping("/member/fines")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberFineController {

    private final FineService fineService;
    private final MemberService memberService;
    private final AuthService authService;

    @GetMapping
    public String myFines(@RequestParam(value = "page", defaultValue = "0") int page,
                          @RequestParam(value = "size", defaultValue = "10") int size,
                          Model model) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        Member member = memberService.findByUserId(currentUser.getId()).orElse(null);

        Page<Fine> fines = Page.empty();
        Page<FinePayment> payments = Page.empty();
        BigDecimal balance = BigDecimal.ZERO;

        if (member != null) {
            fines = fineService.findFinesByMember(member.getId(), PageRequest.of(page, size));
            payments = fineService.findPaymentsByMember(member.getId(), PageRequest.of(page, size));
            balance = fineService.getOutstandingBalanceForMember(member.getId());
        }

        model.addAttribute("fines", fines.getContent());
        model.addAttribute("payments", payments.getContent());
        model.addAttribute("outstandingBalance", balance);
        model.addAttribute("activeMenu", "mem-fines");

        return "member/circulation/fines";
    }
}
