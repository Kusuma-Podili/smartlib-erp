package com.library.erp.controller.member;

import com.library.erp.entity.Member;
import com.library.erp.entity.Reservation;
import com.library.erp.entity.User;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.AuthService;
import com.library.erp.service.MemberService;
import com.library.erp.service.ReservationService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/member/reservations")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberReservationController {

    private final ReservationService reservationService;
    private final MemberService memberService;
    private final AuthService authService;

    @GetMapping
    public String myReservations(@RequestParam(value = "page", defaultValue = "0") int page,
                                 @RequestParam(value = "size", defaultValue = "10") int size,
                                 Model model) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        Member member = memberService.findByUserId(currentUser.getId()).orElse(null);

        Page<Reservation> reservations = Page.empty();
        if (member != null) {
            reservations = reservationService.findReservationsByMember(member.getId(), PageRequest.of(page, size));
        }

        model.addAttribute("reservations", reservations.getContent());
        model.addAttribute("totalPages", reservations.getTotalPages());
        model.addAttribute("currentPage", page);
        model.addAttribute("activeMenu", "mem-reservations");

        return "member/circulation/reservations";
    }

    @PostMapping("/{id}/cancel")
    public String cancelReservation(@PathVariable("id") Long reservationId, RedirectAttributes redirectAttributes) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        Member member = memberService.findByUserId(currentUser.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Member record not found."));

        reservationService.cancelReservation(reservationId, member.getId());
        redirectAttributes.addFlashAttribute("successMessage", "Reservation cancelled.");
        return "redirect:/member/reservations";
    }
}
