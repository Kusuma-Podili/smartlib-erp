package com.library.erp.service;

import java.math.BigDecimal;
import java.util.Map;

public interface DashboardAnalyticsService {
    Map<String, Object> getAdminDashboardStats();
    Map<String, Object> getLibrarianDashboardStats();
    Map<String, Object> getMemberDashboardStats(Long memberId);
}
