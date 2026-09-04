package com.library.erp.repository;

import com.library.erp.entity.BookCopy;
import com.library.erp.entity.enums.CopyStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BookCopyRepository extends JpaRepository<BookCopy, Long> {

    Optional<BookCopy> findByBarcode(String barcode);

    boolean existsByBarcode(String barcode);

    List<BookCopy> findByBookIdOrderByCopyNumberAsc(Long bookId);

    List<BookCopy> findByBookIdAndAvailabilityStatus(Long bookId, CopyStatus status);

    @Query("SELECT bc FROM BookCopy bc WHERE bc.book.id = :bookId AND bc.availabilityStatus = 'AVAILABLE' ORDER BY bc.copyNumber ASC")
    List<BookCopy> findFirstAvailableCopy(@Param("bookId") Long bookId);

    long countByAvailabilityStatus(CopyStatus status);

    @Query("SELECT MAX(bc.copyNumber) FROM BookCopy bc WHERE bc.book.id = :bookId")
    Integer findMaxCopyNumberByBookId(@Param("bookId") Long bookId);
}
