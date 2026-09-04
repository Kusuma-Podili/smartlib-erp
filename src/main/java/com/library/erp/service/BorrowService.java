package com.library.erp.service;

import com.library.erp.dto.circulation.BorrowRequestDto;
import com.library.erp.entity.BorrowRecord;
import com.library.erp.entity.Librarian;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

public interface BorrowService {
    BorrowRecord issueBook(BorrowRequestDto dto, Librarian librarian);
    BorrowRecord renewLoan(Long borrowRecordId);
    Optional<BorrowRecord> findById(Long id);
    List<BorrowRecord> findActiveLoansByMember(Long memberId);
    Page<BorrowRecord> findLoanHistoryByMember(Long memberId, Pageable pageable);
    List<BorrowRecord> findOverdueLoans();
    long countActiveLoansByMember(Long memberId);
    long countOverdueLoans();
    long countLoansToday();
}
