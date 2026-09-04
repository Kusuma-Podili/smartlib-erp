package com.library.erp.controller;

import com.library.erp.dto.auth.RegisterRequestDto;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/**
 * Controller handling user authentication, registration, and access control views.
 */
@Slf4j
@Controller
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @GetMapping("/login")
    public String loginPage(@RequestParam(value = "error", required = false) String error,
                            @RequestParam(value = "logout", required = false) String logout,
                            @RequestParam(value = "registered", required = false) String registered,
                            Model model) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.isAuthenticated() && !(auth instanceof AnonymousAuthenticationToken)) {
            // User is already logged in, redirect based on their role
            return redirectBasedOnRole(auth);
        }

        if (error != null) {
            model.addAttribute("errorMessage", "Invalid username/email or password. Please try again.");
        }
        if (logout != null) {
            model.addAttribute("successMessage", "You have been logged out securely.");
        }
        if (registered != null) {
            model.addAttribute("successMessage", "Registration successful! You can now log in with your credentials.");
        }

        return "auth/login";
    }

    @GetMapping("/register")
    public String registerPage(Model model) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.isAuthenticated() && !(auth instanceof AnonymousAuthenticationToken)) {
            return redirectBasedOnRole(auth);
        }

        if (!model.containsAttribute("registerDto")) {
            model.addAttribute("registerDto", new RegisterRequestDto());
        }
        return "auth/register";
    }

    @PostMapping("/register")
    public String handleRegister(@Valid @ModelAttribute("registerDto") RegisterRequestDto registerDto,
                                 BindingResult bindingResult,
                                 RedirectAttributes redirectAttributes,
                                 Model model) {
        if (!registerDto.getPassword().equals(registerDto.getConfirmPassword())) {
            bindingResult.rejectValue("confirmPassword", "error.registerDto", "Passwords do not match");
        }

        if (bindingResult.hasErrors()) {
            return "auth/register";
        }

        try {
            authService.registerMember(registerDto);
            redirectAttributes.addFlashAttribute("successMessage", "Account registered successfully! Please log in.");
            return "redirect:/login?registered=true";
        } catch (DuplicateResourceException e) {
            model.addAttribute("errorMessage", e.getMessage());
            return "auth/register";
        } catch (Exception e) {
            model.addAttribute("errorMessage", "Registration failed: " + e.getMessage());
            return "auth/register";
        }
    }

    @GetMapping("/access-denied")
    public String accessDenied(Model model) {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null) {
            model.addAttribute("username", auth.getName());
            model.addAttribute("roles", auth.getAuthorities());
        }
        return "error/403";
    }

    private String redirectBasedOnRole(Authentication auth) {
        boolean isAdmin = auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals(RoleName.ROLE_ADMIN.name()));
        if (isAdmin) return "redirect:/admin/dashboard";

        boolean isLibrarian = auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals(RoleName.ROLE_LIBRARIAN.name()));
        if (isLibrarian) return "redirect:/librarian/dashboard";

        return "redirect:/member/dashboard";
    }
}
