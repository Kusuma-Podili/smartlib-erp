package com.library.erp.controller.member;

import com.library.erp.dto.member.MemberProfileDto;
import com.library.erp.entity.Member;
import com.library.erp.entity.Membership;
import com.library.erp.entity.User;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.AuthService;
import com.library.erp.service.MemberService;
import com.library.erp.service.MembershipService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/member/profile")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberProfileController {

    private final AuthService authService;
    private final MemberService memberService;
    private final MembershipService membershipService;

    @GetMapping
    public String viewProfile(Model model) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        Member member = memberService.findByUserId(currentUser.getId()).orElse(null);

        Membership activeMembership = null;
        if (member != null) {
            activeMembership = membershipService.getActiveMembershipForMember(member.getId()).orElse(null);
        }

        MemberProfileDto dto = MemberProfileDto.builder()
                .userId(currentUser.getId())
                .id(member != null ? member.getId() : null)
                .memberCode(member != null ? member.getMemberCode() : "N/A")
                .username(currentUser.getUsername())
                .email(currentUser.getEmail())
                .firstName(currentUser.getFirstName())
                .lastName(currentUser.getLastName())
                .phone(currentUser.getPhone())
                .address(member != null ? member.getAddress() : "")
                .dateOfBirth(member != null ? member.getDateOfBirth() : null)
                .occupation(member != null ? member.getOccupation() : "")
                .membershipTypeName(member != null ? member.getMembershipType().getName() : "Standard")
                .membershipExpiryDate(activeMembership != null ? activeMembership.getExpiryDate() : null)
                .membershipActive(activeMembership != null && !activeMembership.isExpired())
                .build();

        model.addAttribute("profileDto", dto);
        model.addAttribute("activeMenu", "mem-profile");
        return "member/profile/index";
    }

    @PostMapping("/update")
    public String updateProfile(@Valid @ModelAttribute("profileDto") MemberProfileDto dto,
                                BindingResult bindingResult,
                                RedirectAttributes redirectAttributes,
                                Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("activeMenu", "mem-profile");
            return "member/profile/index";
        }

        User currentUser = authService.getCurrentAuthenticatedUser();
        Member member = memberService.findByUserId(currentUser.getId())
                .orElseThrow(() -> new ResourceNotFoundException("Member record not associated with this user account."));

        memberService.updateProfile(member.getId(), dto);
        redirectAttributes.addFlashAttribute("successMessage", "Profile details updated successfully.");
        return "redirect:/member/profile";
    }
}
