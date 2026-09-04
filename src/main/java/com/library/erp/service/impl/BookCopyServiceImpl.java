package com.library.erp.service.impl;

import com.library.erp.entity.BookCopy;
import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.entity.enums.CopyStatus;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.BookCopyRepository;
import com.library.erp.service.BookCopyService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class BookCopyServiceImpl implements BookCopyService {

    private final BookCopyRepository bookCopyRepository;

    @Override
    @Transactional(readOnly = true)
    public Optional<BookCopy> findById(Long id) {
        return bookCopyRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<BookCopy> findByBarcode(String barcode) {
        return bookCopyRepository.findByBarcode(barcode.trim());
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookCopy> findCopiesByBookId(Long bookId) {
        return bookCopyRepository.findByBookIdOrderByCopyNumberAsc(bookId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BookCopy> findAvailableCopiesByBookId(Long bookId) {
        return bookCopyRepository.findByBookIdAndAvailabilityStatus(bookId, CopyStatus.AVAILABLE);
    }

    @Override
    public BookCopy updateCondition(Long copyId, CopyCondition condition) {
        BookCopy copy = bookCopyRepository.findById(copyId)
                .orElseThrow(() -> new ResourceNotFoundException("Book copy not found with id: " + copyId));
        copy.setConditionStatus(condition);
        return bookCopyRepository.save(copy);
    }

    @Override
    public BookCopy updateStatus(Long copyId, CopyStatus status) {
        BookCopy copy = bookCopyRepository.findById(copyId)
                .orElseThrow(() -> new ResourceNotFoundException("Book copy not found with id: " + copyId));
        copy.setAvailabilityStatus(status);
        return bookCopyRepository.save(copy);
    }

    @Override
    public BookCopy markAsLost(Long copyId, String remarks) {
        BookCopy copy = bookCopyRepository.findById(copyId)
                .orElseThrow(() -> new ResourceNotFoundException("Book copy not found with id: " + copyId));
        copy.setAvailabilityStatus(CopyStatus.LOST);
        copy.setConditionStatus(CopyCondition.LOST);
        copy.setRemarks(remarks != null ? remarks : "Marked as lost by librarian");
        return bookCopyRepository.save(copy);
    }

    @Override
    public BookCopy markAsDamaged(Long copyId, String remarks) {
        BookCopy copy = bookCopyRepository.findById(copyId)
                .orElseThrow(() -> new ResourceNotFoundException("Book copy not found with id: " + copyId));
        copy.setAvailabilityStatus(CopyStatus.MAINTENANCE);
        copy.setConditionStatus(CopyCondition.DAMAGED);
        copy.setRemarks(remarks != null ? remarks : "Marked as damaged, sent to repair/maintenance");
        return bookCopyRepository.save(copy);
    }

    @Override
    @Transactional(readOnly = true)
    public long countByStatus(CopyStatus status) {
        return bookCopyRepository.countByAvailabilityStatus(status);
    }

    @Override
    @Transactional(readOnly = true)
    public long countTotalCopies() {
        return bookCopyRepository.count();
    }
}
