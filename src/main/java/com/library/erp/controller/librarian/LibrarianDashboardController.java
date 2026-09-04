package com.library.erp.controller.librarian;

import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/librarian")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianDashboardController {

    private final com.library.erp.service.DashboardAnalyticsService dashboardAnalyticsService;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        java.util.Map<String, Object> stats = dashboardAnalyticsService.getLibrarianDashboardStats();
        model.addAllAttributes(stats);
        model.addAttribute("activeMenu", "lib-dashboard");
        return "librarian/dashboard";
    }
}
