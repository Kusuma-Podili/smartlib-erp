package com.library.erp.controller.admin;

import com.library.erp.entity.AuditLog;
import com.library.erp.service.AuditLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/admin/audit-logs")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminAuditController {

    private final AuditLogService auditLogService;

    @GetMapping
    public String viewAuditLogs(@RequestParam(value = "username", required = false) String username,
                                @RequestParam(value = "action", required = false) String action,
                                @RequestParam(value = "page", defaultValue = "0") int page,
                                @RequestParam(value = "size", defaultValue = "20") int size,
                                Model model) {
        Page<AuditLog> logs = auditLogService.searchLogs(username, action, PageRequest.of(page, size));

        model.addAttribute("logs", logs.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", logs.getTotalPages());
        model.addAttribute("totalElements", logs.getTotalElements());
        model.addAttribute("selectedUser", username);
        model.addAttribute("selectedAction", action);
        model.addAttribute("activeMenu", "admin-audit");

        return "admin/audit/list";
    }
}
