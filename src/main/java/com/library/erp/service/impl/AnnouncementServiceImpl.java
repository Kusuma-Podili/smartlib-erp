package com.library.erp.service.impl;

import com.library.erp.entity.Announcement;
import com.library.erp.entity.User;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.AnnouncementRepository;
import com.library.erp.service.AnnouncementService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional
public class AnnouncementServiceImpl implements AnnouncementService {

    private final AnnouncementRepository announcementRepository;

    @Override
    public Announcement createAnnouncement(String title, String content, String targetRole, LocalDate expiryDate, User creator) {
        Announcement announcement = Announcement.builder()
                .title(title.trim())
                .content(content)
                .targetRole(targetRole != null ? targetRole.toUpperCase() : "ALL")
                .publishDate(LocalDate.now())
                .expiryDate(expiryDate)
                .isPublished(true)
                .createdByUser(creator)
                .build();

        return announcementRepository.save(announcement);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Announcement> getActiveAnnouncementsForRole(String role) {
        return announcementRepository.findActiveAnnouncementsForRole(role, LocalDate.now());
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Announcement> getAllAnnouncements(Pageable pageable) {
        return announcementRepository.findAllByOrderByPublishDateDesc(pageable);
    }

    @Override
    public void deleteAnnouncement(Long id) {
        if (!announcementRepository.existsById(id)) {
            throw new ResourceNotFoundException("Announcement not found with id: " + id);
        }
        announcementRepository.deleteById(id);
    }
}
