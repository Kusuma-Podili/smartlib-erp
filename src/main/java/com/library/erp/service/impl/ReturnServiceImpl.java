package com.library.erp.service.impl;

import com.library.erp.dto.circulation.ReturnProcessDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.*;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.BookCopyRepository;
import com.library.erp.repository.BorrowRecordRepository;
import com.library.erp.repository.ReturnRecordRepository;
import com.library.erp.service.FineService;
import com.library.erp.service.ReservationService;
import com.library.erp.service.ReturnService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class ReturnServiceImpl implements ReturnService {

    private final BorrowRecordRepository borrowRecordRepository;
    private final ReturnRecordRepository returnRecordRepository;
    private final BookCopyRepository bookCopyRepository;
    private final FineService fineService;
    private final ReservationService reservationService;

    @Override
    public ReturnRecord processReturn(ReturnProcessDto dto, Librarian librarian) {
        BorrowRecord borrowRecord = borrowRecordRepository.findActiveLoanByBarcode(dto.getBarcode().trim())
                .orElseThrow(() -> new ResourceNotFoundException(
                        "No active loan found for barcode: " + dto.getBarcode() + ". The copy might already be returned or barcode is invalid."
                ));

        LocalDate returnDate = LocalDate.now();
        LocalDate dueDate = borrowRecord.getDueDate();
        long daysLate = 0;
        BigDecimal totalFineAssessed = BigDecimal.ZERO;

        if (returnDate.isAfter(dueDate)) {
            daysLate = ChronoUnit.DAYS.between(dueDate, returnDate);
            int gracePeriod = borrowRecord.getMember().getMembershipType().getGracePeriodDays();
            long billableDays = Math.max(0, daysLate - gracePeriod);

            if (billableDays > 0) {
                BigDecimal fineRate = borrowRecord.getMember().getMembershipType().getFinePerDay();
                totalFineAssessed = fineRate.multiply(BigDecimal.valueOf(billableDays));

                // Generate overdue fine
                fineService.createFine(
                        borrowRecord,
                        borrowRecord.getMember(),
                        FineType.LATE_RETURN,
                        totalFineAssessed,
                        String.format("Overdue by %d days (%d days billable after %d grace days)", daysLate, billableDays, gracePeriod)
                );
            }
        }

        // Handle condition charges
        BookCopy copy = borrowRecord.getBookCopy();
        CopyCondition returnedCondition = dto.getCondition() != null ? dto.getCondition() : CopyCondition.GOOD;
        copy.setConditionStatus(returnedCondition);

        if (returnedCondition == CopyCondition.DAMAGED || dto.getAdditionalDamageCharge() != null) {
            BigDecimal damageCharge = dto.getAdditionalDamageCharge() != null ? dto.getAdditionalDamageCharge() : BigDecimal.valueOf(150.00);
            totalFineAssessed = totalFineAssessed.add(damageCharge);
            fineService.createFine(
                    borrowRecord,
                    borrowRecord.getMember(),
                    FineType.DAMAGED_BOOK,
                    damageCharge,
                    "Damage penalty: " + (dto.getRemarks() != null ? dto.getRemarks() : "Damaged copy on return")
            );
            copy.setAvailabilityStatus(CopyStatus.MAINTENANCE);
        } else {
            copy.setAvailabilityStatus(CopyStatus.AVAILABLE);
        }

        bookCopyRepository.save(copy);

        // Mark borrow record as RETURNED
        borrowRecord.setStatus(BorrowStatus.RETURNED);
        borrowRecordRepository.save(borrowRecord);

        // Save return record
        ReturnRecord returnRecord = ReturnRecord.builder()
                .borrowRecord(borrowRecord)
                .librarian(librarian)
                .returnDate(returnDate)
                .daysOverdue((int) daysLate)
                .fineAssessed(totalFineAssessed)
                .returnedCondition(returnedCondition)
                .remarks(dto.getRemarks())
                .build();

        ReturnRecord saved = returnRecordRepository.save(returnRecord);

        // Notify next member in reservation queue if copy is available!
        if (copy.getAvailabilityStatus() == CopyStatus.AVAILABLE) {
            reservationService.notifyNextInQueue(copy.getBook().getId());
        }

        log.info("Processed return for copy {} (Book: '{}'). Overdue days: {}, Assessed fine: ₹{}",
                copy.getBarcode(), copy.getBook().getTitle(), daysLate, totalFineAssessed);

        return saved;
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<ReturnRecord> findById(Long id) {
        return returnRecordRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<ReturnRecord> findAllReturns(Pageable pageable) {
        return returnRecordRepository.findAllByOrderByReturnDateDesc(pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public long countReturnsToday() {
        return returnRecordRepository.countByReturnDate(LocalDate.now());
    }
}
