package com.library.erp.service;

import com.library.erp.entity.BookCopy;
import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.entity.enums.CopyStatus;

import java.util.List;
import java.util.Optional;

public interface BookCopyService {
    Optional<BookCopy> findById(Long id);
    Optional<BookCopy> findByBarcode(String barcode);
    List<BookCopy> findCopiesByBookId(Long bookId);
    List<BookCopy> findAvailableCopiesByBookId(Long bookId);
    BookCopy updateCondition(Long copyId, CopyCondition condition);
    BookCopy updateStatus(Long copyId, CopyStatus status);
    BookCopy markAsLost(Long copyId, String remarks);
    BookCopy markAsDamaged(Long copyId, String remarks);
    long countByStatus(CopyStatus status);
    long countTotalCopies();
}
