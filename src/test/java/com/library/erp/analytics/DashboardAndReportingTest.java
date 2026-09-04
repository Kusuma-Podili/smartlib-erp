package com.library.erp.analytics;

import com.library.erp.entity.AuditLog;
import com.library.erp.entity.Notification;
import com.library.erp.entity.User;
import com.library.erp.entity.enums.NotificationType;
import com.library.erp.repository.UserRepository;
import com.library.erp.service.*;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.io.ByteArrayOutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class DashboardAndReportingTest {

    @Autowired
    private AuditLogService auditLogService;

    @Autowired
    private NotificationService notificationService;

    @Autowired
    private DashboardAnalyticsService dashboardAnalyticsService;

    @Autowired
    private CsvExportService csvExportService;

    @Autowired
    private PdfReportService pdfReportService;

    @Autowired
    private UserRepository userRepository;

    @Test
    @DisplayName("Test 1: Audit logging records actions and supports filtered search")
    void auditLoggingSearch() {
        String testUser = "auditor_" + System.currentTimeMillis();
        auditLogService.logAction(testUser, "BOOK_CREATED", "Book", 999L, "Created title", "127.0.0.1");

        Page<AuditLog> results = auditLogService.searchLogs(testUser, "BOOK_CREATED", PageRequest.of(0, 10));
        assertThat(results.getContent()).isNotEmpty();
        AuditLog entry = results.getContent().get(0);
        assertThat(entry.getUsername()).isEqualTo(testUser);
        assertThat(entry.getAction()).isEqualTo("BOOK_CREATED");
    }

    @Test
    @DisplayName("Test 2: Notification service delivers alerts and counts unread messages")
    void notificationDeliveryWorkflow() {
        User user = userRepository.findByUsername("member").orElseThrow();

        Notification notif = notificationService.sendNotification(
                user.getId(),
                "Book Due Reminder",
                "Your book is due tomorrow.",
                NotificationType.DUE_REMINDER,
                "/member/loans"
        );

        assertThat(notif.getId()).isNotNull();
        assertThat(notif.isRead()).isFalse();

        long unreadCount = notificationService.countUnreadNotifications(user.getId());
        assertThat(unreadCount).isGreaterThanOrEqualTo(1);

        // Mark read
        notificationService.markAsRead(notif.getId(), user.getId());
        assertThat(notificationService.countUnreadNotifications(user.getId())).isLessThan(unreadCount);
    }

    @Test
    @DisplayName("Test 3: Dashboard analytics aggregates metrics for executive oversight")
    void dashboardAnalyticsDataAggregation() {
        Map<String, Object> adminStats = dashboardAnalyticsService.getAdminDashboardStats();
        assertThat(adminStats).containsKey("totalBooks");
        assertThat(adminStats).containsKey("activeMembers");
        assertThat(adminStats).containsKey("finesCollected");
        assertThat(adminStats).containsKey("monthLabels");

        Map<String, Object> libStats = dashboardAnalyticsService.getLibrarianDashboardStats();
        assertThat(libStats).containsKey("issuedToday");
        assertThat(libStats).containsKey("pendingHolds");
    }

    @Test
    @DisplayName("Test 4: CSV exporter streams formatted data with headers")
    void csvExportProducesValidData() {
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);

        csvExportService.exportBooksCsv(pw);
        String booksCsv = sw.toString();
        assertThat(booksCsv).contains("ISBN,Title,Category");

        StringWriter swMembers = new StringWriter();
        csvExportService.exportMembersCsv(new PrintWriter(swMembers));
        assertThat(swMembers.toString()).contains("MemberCode,FullName");
    }

    @Test
    @DisplayName("Test 5: PDF reporting produces binary document stream with non-zero bytes")
    void pdfReportGeneratesDocumentStream() throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        pdfReportService.generateBookCatalogPdf(baos);

        byte[] pdfBytes = baos.toByteArray();
        assertThat(pdfBytes).isNotEmpty();
        // PDF files start with magic header %PDF
        assertThat(new String(pdfBytes, 0, 4)).isEqualTo("%PDF");
    }
}
