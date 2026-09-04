package com.library.erp.controller.admin;

import com.library.erp.dto.catalog.PublisherDto;
import com.library.erp.entity.Publisher;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.service.PublisherService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/admin/publishers")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminPublisherController {

    private final PublisherService publisherService;

    @GetMapping
    public String listPublishers(Model model) {
        model.addAttribute("publishers", publisherService.findAllPublishers());
        if (!model.containsAttribute("publisherDto")) {
            model.addAttribute("publisherDto", new PublisherDto());
        }
        model.addAttribute("activeMenu", "admin-publishers");
        return "admin/publishers/list";
    }

    @PostMapping
    public String createPublisher(@Valid @ModelAttribute("publisherDto") PublisherDto publisherDto,
                                  BindingResult bindingResult,
                                  RedirectAttributes redirectAttributes,
                                  Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("publishers", publisherService.findAllPublishers());
            model.addAttribute("activeMenu", "admin-publishers");
            return "admin/publishers/list";
        }

        try {
            Publisher created = publisherService.createPublisher(publisherDto);
            redirectAttributes.addFlashAttribute("successMessage", "Publisher '" + created.getName() + "' created successfully.");
            return "redirect:/admin/publishers";
        } catch (DuplicateResourceException e) {
            redirectAttributes.addFlashAttribute("errorMessage", e.getMessage());
            return "redirect:/admin/publishers";
        }
    }
}
