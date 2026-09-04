package com.library.erp.controller.admin;

import com.library.erp.entity.enums.RoleName;
import com.library.erp.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminDashboardController {

    private final com.library.erp.service.DashboardAnalyticsService dashboardAnalyticsService;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        java.util.Map<String, Object> stats = dashboardAnalyticsService.getAdminDashboardStats();
        model.addAllAttributes(stats);
        model.addAttribute("activeMenu", "admin-dashboard");
        return "admin/dashboard";
    }
}
