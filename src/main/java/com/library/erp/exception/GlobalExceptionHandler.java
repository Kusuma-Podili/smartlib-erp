package com.library.erp.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/**
 * Centralized exception handling across all controllers.
 */
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public String handleNotFound(ResourceNotFoundException ex, Model model, HttpServletRequest request) {
        model.addAttribute("errorMessage", ex.getMessage());
        model.addAttribute("status", 404);
        model.addAttribute("path", request.getRequestURI());
        return "error/404";
    }

    @ExceptionHandler(BusinessRuleViolationException.class)
    public String handleBusinessRule(BusinessRuleViolationException ex, RedirectAttributes redirectAttributes, HttpServletRequest request) {
        redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
        String referer = request.getHeader("Referer");
        return "redirect:" + (referer != null ? referer : "/");
    }

    @ExceptionHandler(Exception.class)
    public String handleGeneralError(Exception ex, Model model, HttpServletRequest request) {
        model.addAttribute("errorMessage", "An unexpected system error occurred: " + ex.getMessage());
        model.addAttribute("status", 500);
        model.addAttribute("path", request.getRequestURI());
        return "error/500";
    }
}
