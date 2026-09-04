package com.library.erp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "announcements")
public class Announcement extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "title", nullable = false, length = 150)
    private String title;

    @Column(name = "content", nullable = false, columnDefinition = "TEXT")
    private String content;

    @Column(name = "target_role", length = 50)
    @Builder.Default
    private String targetRole = "ALL"; // ALL, MEMBER, LIBRARIAN

    @Column(name = "is_published", nullable = false)
    @Builder.Default
    private boolean isPublished = true;

    @Column(name = "publish_date")
    @Builder.Default
    private LocalDate publishDate = LocalDate.now();

    @Column(name = "expiry_date")
    private LocalDate expiryDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "created_by_user_id")
    private User createdByUser;
}
