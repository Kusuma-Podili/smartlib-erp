package com.library.erp.controller.member;

import com.library.erp.entity.Notification;
import com.library.erp.entity.User;
import com.library.erp.service.AuthService;
import com.library.erp.service.NotificationService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/member/notifications")
@PreAuthorize("hasRole('MEMBER')")
@RequiredArgsConstructor
public class MemberNotificationController {

    private final NotificationService notificationService;
    private final AuthService authService;

    @GetMapping
    public String myNotifications(@RequestParam(value = "page", defaultValue = "0") int page,
                                  @RequestParam(value = "size", defaultValue = "15") int size,
                                  Model model) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        Page<Notification> notifs = notificationService.getUserNotifications(currentUser.getId(), PageRequest.of(page, size));

        model.addAttribute("notifications", notifs.getContent());
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", notifs.getTotalPages());
        model.addAttribute("unreadCount", notificationService.countUnreadNotifications(currentUser.getId()));
        model.addAttribute("activeMenu", "mem-notifications");

        return "member/notifications/index";
    }

    @PostMapping("/{id}/read")
    public String markRead(@PathVariable("id") Long id) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        notificationService.markAsRead(id, currentUser.getId());
        return "redirect:/member/notifications";
    }

    @PostMapping("/read-all")
    public String markAllRead(RedirectAttributes redirectAttributes) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        notificationService.markAllAsRead(currentUser.getId());
        redirectAttributes.addFlashAttribute("successMessage", "All notifications marked as read.");
        return "redirect:/member/notifications";
    }
}
