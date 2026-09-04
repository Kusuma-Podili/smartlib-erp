package com.library.erp.controller;

import com.library.erp.entity.enums.RoleName;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Root routing controller redirecting to role dashboards or the login page.
 */
@Controller
public class HomeController {

    @GetMapping("/")
    public String index() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated() || auth instanceof AnonymousAuthenticationToken) {
            return "redirect:/login";
        }

        boolean isAdmin = auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals(RoleName.ROLE_ADMIN.name()));
        if (isAdmin) return "redirect:/admin/dashboard";

        boolean isLibrarian = auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals(RoleName.ROLE_LIBRARIAN.name()));
        if (isLibrarian) return "redirect:/librarian/dashboard";

        return "redirect:/member/dashboard";
    }
}
