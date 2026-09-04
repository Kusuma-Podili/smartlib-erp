package com.library.erp.repository;

import com.library.erp.entity.Announcement;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface AnnouncementRepository extends JpaRepository<Announcement, Long> {

    @Query("SELECT a FROM Announcement a WHERE a.isPublished = true " +
           "AND (a.expiryDate IS NULL OR a.expiryDate >= :today) " +
           "AND (a.targetRole = 'ALL' OR a.targetRole = :role) " +
           "ORDER BY a.publishDate DESC")
    List<Announcement> findActiveAnnouncementsForRole(@Param("role") String role, @Param("today") LocalDate today);

    Page<Announcement> findAllByOrderByPublishDateDesc(Pageable pageable);
}
