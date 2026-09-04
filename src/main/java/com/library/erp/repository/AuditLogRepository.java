package com.library.erp.repository;

import com.library.erp.entity.AuditLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {

    @Query("SELECT a FROM AuditLog a WHERE (:username IS NULL OR LOWER(a.username) LIKE LOWER(CONCAT('%', :username, '%'))) " +
           "AND (:action IS NULL OR a.action = :action) ORDER BY a.timestamp DESC")
    Page<AuditLog> searchLogs(@Param("username") String username,
                              @Param("action") String action,
                              Pageable pageable);
}
