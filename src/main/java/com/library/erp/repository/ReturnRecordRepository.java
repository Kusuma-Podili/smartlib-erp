package com.library.erp.repository;

import com.library.erp.entity.ReturnRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

@Repository
public interface ReturnRecordRepository extends JpaRepository<ReturnRecord, Long> {
    long countByReturnDate(LocalDate returnDate);
    Page<ReturnRecord> findAllByOrderByReturnDateDesc(Pageable pageable);
}
