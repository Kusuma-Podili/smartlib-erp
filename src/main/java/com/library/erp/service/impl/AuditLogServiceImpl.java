package com.library.erp.service.impl;

import com.library.erp.entity.AuditLog;
import com.library.erp.repository.AuditLogRepository;
import com.library.erp.service.AuditLogService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class AuditLogServiceImpl implements AuditLogService {

    private final AuditLogRepository auditLogRepository;

    @Override
    public AuditLog logAction(String username, String action, String entityName, Long entityId, String description, String ipAddress) {
        AuditLog auditLog = AuditLog.builder()
                .username(username != null ? username : "SYSTEM")
                .action(action)
                .entityName(entityName)
                .entityId(entityId)
                .description(description)
                .ipAddress(ipAddress != null ? ipAddress : "127.0.0.1")
                .timestamp(LocalDateTime.now())
                .build();

        AuditLog saved = auditLogRepository.save(auditLog);
        log.info("[AUDIT] User '{}' performed '{}' on entity '{}' (id: {})", username, action, entityName, entityId);
        return saved;
    }

    @Override
    @Transactional(readOnly = true)
    public Page<AuditLog> searchLogs(String username, String action, Pageable pageable) {
        String cleanUser = (username != null && !username.isBlank()) ? username.trim() : null;
        String cleanAction = (action != null && !action.isBlank()) ? action.trim() : null;
        return auditLogRepository.searchLogs(cleanUser, cleanAction, pageable);
    }
}
