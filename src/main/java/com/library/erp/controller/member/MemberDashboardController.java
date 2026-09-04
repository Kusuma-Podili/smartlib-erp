package com.library.erp.controller.member;

import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/member")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberDashboardController {

    private final com.library.erp.service.DashboardAnalyticsService dashboardAnalyticsService;
    private final com.library.erp.service.MemberService memberService;
    private final com.library.erp.service.AuthService authService;

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        com.library.erp.entity.User user = authService.getCurrentAuthenticatedUser();
        Long memberId = memberService.findByUserId(user.getId()).map(com.library.erp.entity.Member::getId).orElse(null);

        java.util.Map<String, Object> stats = dashboardAnalyticsService.getMemberDashboardStats(memberId);
        model.addAllAttributes(stats);
        model.addAttribute("activeMenu", "mem-dashboard");
        return "member/dashboard";
    }
}
