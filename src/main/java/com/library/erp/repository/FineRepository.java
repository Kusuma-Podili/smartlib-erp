package com.library.erp.repository;

import com.library.erp.entity.Fine;
import com.library.erp.entity.enums.FineStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

@Repository
public interface FineRepository extends JpaRepository<Fine, Long> {

    List<Fine> findByMemberIdAndStatusIn(Long memberId, List<FineStatus> statuses);

    Page<Fine> findByMemberIdOrderByCreatedAtDesc(Long memberId, Pageable pageable);

    @Query("SELECT COALESCE(SUM(f.amount - f.paidAmount), 0) FROM Fine f WHERE f.member.id = :memberId AND f.status IN ('UNPAID', 'PARTIALLY_PAID')")
    BigDecimal calculateOutstandingBalanceByMemberId(@Param("memberId") Long memberId);

    @Query("SELECT COALESCE(SUM(f.amount - f.paidAmount), 0) FROM Fine f WHERE f.status IN ('UNPAID', 'PARTIALLY_PAID')")
    BigDecimal calculateTotalUnpaidFines();

    @Query("SELECT COALESCE(SUM(f.paidAmount), 0) FROM Fine f")
    BigDecimal calculateTotalCollectedFines();

    long countByStatus(FineStatus status);
}
