package com.library.erp.service;

import com.library.erp.entity.AuditLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

public interface AuditLogService {
    AuditLog logAction(String username, String action, String entityName, Long entityId, String description, String ipAddress);
    Page<AuditLog> searchLogs(String username, String action, Pageable pageable);
}
