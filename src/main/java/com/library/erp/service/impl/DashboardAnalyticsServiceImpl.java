package com.library.erp.service.impl;

import com.library.erp.entity.enums.CopyStatus;
import com.library.erp.entity.enums.ReservationStatus;
import com.library.erp.repository.*;
import com.library.erp.service.DashboardAnalyticsService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class DashboardAnalyticsServiceImpl implements DashboardAnalyticsService {

    private final BookRepository bookRepository;
    private final BookCopyRepository bookCopyRepository;
    private final MemberRepository memberRepository;
    private final MembershipRepository membershipRepository;
    private final BorrowRecordRepository borrowRecordRepository;
    private final ReturnRecordRepository returnRecordRepository;
    private final ReservationRepository reservationRepository;
    private final FineRepository fineRepository;
    private final CategoryRepository categoryRepository;

    @Override
    public Map<String, Object> getAdminDashboardStats() {
        Map<String, Object> stats = new HashMap<>();

        long totalBooks = bookRepository.count();
        long totalCopies = bookCopyRepository.count();
        long availableCopies = bookCopyRepository.countByAvailabilityStatus(CopyStatus.AVAILABLE);
        long issuedCopies = bookCopyRepository.countByAvailabilityStatus(CopyStatus.BORROWED);

        long totalMembers = memberRepository.count();
        long activeMembers = memberRepository.countByStatus(com.library.erp.entity.enums.UserStatus.ACTIVE);
        long expiredMemberships = membershipRepository.countByStatus(com.library.erp.entity.enums.MembershipStatus.EXPIRED);

        long overdueLoans = borrowRecordRepository.countOverdueLoans(LocalDate.now());
        long pendingReservations = reservationRepository.countByStatus(ReservationStatus.PENDING);

        BigDecimal unpaidFines = fineRepository.calculateTotalUnpaidFines();
        BigDecimal collectedFines = fineRepository.calculateTotalCollectedFines();

        stats.put("totalBooks", totalBooks);
        stats.put("totalCopies", totalCopies);
        stats.put("availableCopies", availableCopies);
        stats.put("issuedCopies", issuedCopies);
        stats.put("totalMembers", totalMembers);
        stats.put("activeMembers", activeMembers);
        stats.put("expiredMemberships", expiredMemberships);
        stats.put("overdueLoans", overdueLoans);
        stats.put("pendingReservations", pendingReservations);
        stats.put("unpaidFines", unpaidFines != null ? unpaidFines : BigDecimal.ZERO);
        stats.put("finesCollected", collectedFines != null ? collectedFines : BigDecimal.ZERO);

        // Monthly trends labels (last 6 months)
        List<String> monthLabels = new ArrayList<>();
        List<Long> borrowTrends = new ArrayList<>();
        List<Long> returnTrends = new ArrayList<>();

        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("MMM yyyy");
        for (int i = 5; i >= 0; i--) {
            LocalDate m = LocalDate.now().minusMonths(i);
            monthLabels.add(m.format(dtf));
            borrowTrends.add(borrowRecordRepository.count());
            returnTrends.add(returnRecordRepository.count());
        }

        stats.put("monthLabels", monthLabels);
        stats.put("borrowTrends", borrowTrends);
        stats.put("returnTrends", returnTrends);

        return stats;
    }

    @Override
    public Map<String, Object> getLibrarianDashboardStats() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("issuedToday", borrowRecordRepository.countByBorrowDate(LocalDate.now()));
        stats.put("returnedToday", returnRecordRepository.countByReturnDate(LocalDate.now()));
        stats.put("pendingHolds", reservationRepository.countByStatus(ReservationStatus.PENDING));
        BigDecimal unpaid = fineRepository.calculateTotalUnpaidFines();
        stats.put("unpaidFines", unpaid != null ? unpaid : BigDecimal.ZERO);
        stats.put("overdueCount", borrowRecordRepository.countOverdueLoans(LocalDate.now()));
        return stats;
    }

    @Override
    public Map<String, Object> getMemberDashboardStats(Long memberId) {
        Map<String, Object> stats = new HashMap<>();
        if (memberId == null) {
            stats.put("borrowedCount", 0);
            stats.put("reservationCount", 0);
            stats.put("outstandingFine", BigDecimal.ZERO);
            stats.put("remainingQuota", 3);
            return stats;
        }

        long borrowed = borrowRecordRepository.countActiveLoansByMemberId(memberId);
        long reservations = reservationRepository.countActiveReservationsByMemberId(memberId);
        BigDecimal outstanding = fineRepository.calculateOutstandingBalanceByMemberId(memberId);

        int limit = memberRepository.findById(memberId)
                .map(m -> m.getMembershipType().getBorrowingLimit())
                .orElse(3);

        stats.put("borrowedCount", borrowed);
        stats.put("reservationCount", reservations);
        stats.put("outstandingFine", outstanding != null ? outstanding : BigDecimal.ZERO);
        stats.put("remainingQuota", Math.max(0, limit - borrowed));

        return stats;
    }
}
