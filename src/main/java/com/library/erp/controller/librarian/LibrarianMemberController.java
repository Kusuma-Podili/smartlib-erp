package com.library.erp.controller.librarian;

import com.library.erp.dto.member.MemberRegistrationDto;
import com.library.erp.entity.Member;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.MemberService;
import com.library.erp.service.MembershipService;
import com.library.erp.service.MembershipTypeService;
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
@RequestMapping("/librarian/members")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianMemberController {

    private final MemberService memberService;
    private final MembershipService membershipService;
    private final MembershipTypeService membershipTypeService;

    @GetMapping
    public String listMembers(@RequestParam(value = "query", required = false) String query,
                              @RequestParam(value = "page", defaultValue = "0") int page,
                              @RequestParam(value = "size", defaultValue = "10") int size,
                              Model model) {
        Page<Member> memberPage = memberService.searchMembers(query, PageRequest.of(page, size, Sort.by("id").descending()));

        model.addAttribute("members", memberPage.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", memberPage.getTotalPages());
        model.addAttribute("totalElements", memberPage.getTotalElements());
        model.addAttribute("query", query);
        model.addAttribute("activeMenu", "lib-members");

        return "librarian/members/list";
    }

    @GetMapping("/new")
    public String newMemberForm(Model model) {
        if (!model.containsAttribute("memberDto")) {
            model.addAttribute("memberDto", new MemberRegistrationDto());
        }
        model.addAttribute("membershipTypes", membershipTypeService.findAllMembershipTypes());
        model.addAttribute("activeMenu", "lib-members");
        return "librarian/members/form";
    }

    @PostMapping
    public String saveMember(@Valid @ModelAttribute("memberDto") MemberRegistrationDto dto,
                             BindingResult bindingResult,
                             RedirectAttributes redirectAttributes,
                             Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("membershipTypes", membershipTypeService.findAllMembershipTypes());
            model.addAttribute("activeMenu", "lib-members");
            return "librarian/members/form";
        }

        try {
            Member saved = memberService.registerMember(dto);
            redirectAttributes.addFlashAttribute("successMessage",
                    "Member registered successfully! Assigned Member ID: " + saved.getMemberCode());
            return "redirect:/librarian/members/" + saved.getId();
        } catch (DuplicateResourceException e) {
            model.addAttribute("errorMessage", e.getMessage());
            model.addAttribute("membershipTypes", membershipTypeService.findAllMembershipTypes());
            model.addAttribute("activeMenu", "lib-members");
            return "librarian/members/form";
        }
    }

    @GetMapping("/{id}")
    public String viewMember(@PathVariable("id") Long id, Model model) {
        Member member = memberService.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + id));

        model.addAttribute("member", member);
        model.addAttribute("activeMembership", membershipService.getActiveMembershipForMember(id).orElse(null));
        model.addAttribute("activeMenu", "lib-members");
        return "librarian/members/view";
    }

    @PostMapping("/{id}/renew")
    public String renewMembership(@PathVariable("id") Long id,
                                  @RequestParam(value = "months", defaultValue = "12") int months,
                                  RedirectAttributes redirectAttributes) {
        membershipService.renewMembership(id, months);
        redirectAttributes.addFlashAttribute("successMessage", "Membership extended by " + months + " months.");
        return "redirect:/librarian/members/" + id;
    }
}
