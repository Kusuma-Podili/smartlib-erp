package com.library.erp.repository;

import com.library.erp.entity.BorrowRecord;
import com.library.erp.entity.enums.BorrowStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface BorrowRecordRepository extends JpaRepository<BorrowRecord, Long> {

    List<BorrowRecord> findByMemberIdAndStatusIn(Long memberId, List<BorrowStatus> statuses);

    Page<BorrowRecord> findByMemberIdOrderByBorrowDateDesc(Long memberId, Pageable pageable);

    @Query("SELECT COUNT(br) FROM BorrowRecord br WHERE br.member.id = :memberId AND br.status = 'ISSUED'")
    long countActiveLoansByMemberId(@Param("memberId") Long memberId);

    @Query("SELECT br FROM BorrowRecord br WHERE br.status = 'ISSUED' AND br.dueDate < :currentDate")
    List<BorrowRecord> findOverdueLoans(@Param("currentDate") LocalDate currentDate);

    @Query("SELECT COUNT(br) FROM BorrowRecord br WHERE br.status = 'ISSUED' AND br.dueDate < :currentDate")
    long countOverdueLoans(@Param("currentDate") LocalDate currentDate);

    @Query("SELECT br FROM BorrowRecord br WHERE br.bookCopy.barcode = :barcode AND br.status = 'ISSUED'")
    Optional<BorrowRecord> findActiveLoanByBarcode(@Param("barcode") String barcode);

    long countByBorrowDate(LocalDate borrowDate);

    long countByStatus(BorrowStatus status);
}
