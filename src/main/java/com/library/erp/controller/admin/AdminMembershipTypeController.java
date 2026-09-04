package com.library.erp.controller.admin;

import com.library.erp.dto.member.MembershipTypeDto;
import com.library.erp.entity.MembershipType;
import com.library.erp.service.MembershipTypeService;
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
@RequestMapping("/admin/membership-types")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminMembershipTypeController {

    private final MembershipTypeService membershipTypeService;

    @GetMapping
    public String listTypes(Model model) {
        model.addAttribute("types", membershipTypeService.findAllMembershipTypes());
        if (!model.containsAttribute("typeDto")) {
            model.addAttribute("typeDto", new MembershipTypeDto());
        }
        model.addAttribute("activeMenu", "admin-membership-types");
        return "admin/membership_types/list";
    }

    @PostMapping
    public String saveType(@Valid @ModelAttribute("typeDto") MembershipTypeDto typeDto,
                           BindingResult bindingResult,
                           RedirectAttributes redirectAttributes,
                           Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("types", membershipTypeService.findAllMembershipTypes());
            model.addAttribute("activeMenu", "admin-membership-types");
            return "admin/membership_types/list";
        }

        MembershipType saved = membershipTypeService.createMembershipType(typeDto);
        redirectAttributes.addFlashAttribute("successMessage", "Membership tier '" + saved.getName() + "' created successfully.");
        return "redirect:/admin/membership-types";
    }
}
