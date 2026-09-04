package com.library.erp.controller.admin;

import com.library.erp.entity.Member;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.service.MemberService;
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
@RequestMapping("/admin/members")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminMemberController {

    private final MemberService memberService;

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
        model.addAttribute("activeMenu", "admin-members");

        return "admin/members/list";
    }

    @GetMapping("/{id}")
    public String viewMember(@PathVariable("id") Long id, Model model) {
        Member member = memberService.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + id));

        model.addAttribute("member", member);
        model.addAttribute("activeMenu", "admin-members");
        return "admin/members/view";
    }

    @PostMapping("/{id}/toggle-status")
    public String toggleStatus(@PathVariable("id") Long id, RedirectAttributes redirectAttributes) {
        Member member = memberService.toggleMemberStatus(id);
        redirectAttributes.addFlashAttribute("successMessage",
                "Member " + member.getMemberCode() + " status is now " + member.getUser().getStatus());
        return "redirect:/admin/members/" + id;
    }
}
