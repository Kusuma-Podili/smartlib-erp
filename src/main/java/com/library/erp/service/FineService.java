package com.library.erp.service;

import com.library.erp.dto.circulation.FinePaymentDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.FineType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

public interface FineService {
    Fine createFine(BorrowRecord borrowRecord, Member member, FineType fineType, BigDecimal amount, String reason);
    FinePayment recordPayment(FinePaymentDto dto, Librarian librarian);
    Fine waiveFine(Long fineId, String reason);
    Optional<Fine> findById(Long id);
    List<Fine> findUnpaidFinesByMember(Long memberId);
    Page<Fine> findFinesByMember(Long memberId, Pageable pageable);
    Page<FinePayment> findPaymentsByMember(Long memberId, Pageable pageable);
    BigDecimal getOutstandingBalanceForMember(Long memberId);
    BigDecimal getTotalUnpaidFines();
    BigDecimal getTotalCollectedFines();
}
