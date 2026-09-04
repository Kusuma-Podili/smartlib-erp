package com.library.erp.service;

import com.library.erp.entity.Announcement;
import com.library.erp.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.time.LocalDate;
import java.util.List;

public interface AnnouncementService {
    Announcement createAnnouncement(String title, String content, String targetRole, LocalDate expiryDate, User creator);
    List<Announcement> getActiveAnnouncementsForRole(String role);
    Page<Announcement> getAllAnnouncements(Pageable pageable);
    void deleteAnnouncement(Long id);
}
