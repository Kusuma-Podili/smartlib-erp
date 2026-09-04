package com.library.erp.service;

import com.library.erp.entity.Notification;
import com.library.erp.entity.enums.NotificationType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface NotificationService {
    Notification sendNotification(Long userId, String title, String message, NotificationType type, String linkUrl);
    Page<Notification> getUserNotifications(Long userId, Pageable pageable);
    List<Notification> getRecentUnread(Long userId);
    long countUnreadNotifications(Long userId);
    void markAsRead(Long notificationId, Long userId);
    void markAllAsRead(Long userId);
}
