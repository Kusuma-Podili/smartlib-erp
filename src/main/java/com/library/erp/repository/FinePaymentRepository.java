package com.library.erp.repository;

import com.library.erp.entity.FinePayment;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;

@Repository
public interface FinePaymentRepository extends JpaRepository<FinePayment, Long> {

    Page<FinePayment> findByMemberIdOrderByPaymentDateDesc(Long memberId, Pageable pageable);

    @Query("SELECT COALESCE(SUM(fp.amountPaid), 0) FROM FinePayment fp WHERE CAST(fp.paymentDate as date) = :date")
    BigDecimal calculateTotalPaymentsOnDate(@Param("date") LocalDate date);
}
