package com.library.erp.service.impl;

import com.library.erp.dto.circulation.BorrowRequestDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.BorrowStatus;
import com.library.erp.entity.enums.CopyStatus;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.*;
import com.library.erp.service.BorrowService;
import com.library.erp.service.MembershipService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class BorrowServiceImpl implements BorrowService {

    private final BorrowRecordRepository borrowRecordRepository;
    private final MemberRepository memberRepository;
    private final BookCopyRepository bookCopyRepository;
    private final MembershipService membershipService;

    @Override
    public BorrowRecord issueBook(BorrowRequestDto dto, Librarian librarian) {
        Member member = memberRepository.findByMemberCode(dto.getMemberCode().trim())
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with code: " + dto.getMemberCode()));

        // Business Rule 1: Member account must be active and membership not expired
        if (!membershipService.isMemberEligibleToBorrow(member.getId())) {
            throw new BusinessRuleViolationException(
                    "Member account is inactive or their membership subscription has expired. Please renew first."
            );
        }

        // Business Rule 2: Member cannot exceed their borrowing limit
        long activeLoans = borrowRecordRepository.countActiveLoansByMemberId(member.getId());
        int limit = member.getEffectiveBorrowingLimit();
        if (activeLoans >= limit) {
            throw new BusinessRuleViolationException(
                    "Borrowing limit reached! Current tier allows max " + limit + " active book loans (currently holds " + activeLoans + ")."
            );
        }

        // Business Rule 3: Physical copy must exist and be AVAILABLE
        BookCopy copy = bookCopyRepository.findByBarcode(dto.getBarcode().trim())
                .orElseThrow(() -> new ResourceNotFoundException("Book copy not found with barcode: " + dto.getBarcode()));

        if (copy.getAvailabilityStatus() != CopyStatus.AVAILABLE) {
            throw new BusinessRuleViolationException(
                    "Physical copy '" + copy.getBarcode() + "' is not available (Current status: " + copy.getAvailabilityStatus() + ")."
            );
        }

        // Calculate due date based on member's membership tier
        int durationDays = member.getMembershipType().getBorrowDurationDays();
        LocalDate borrowDate = LocalDate.now();
        LocalDate dueDate = borrowDate.plusDays(durationDays);

        // Update physical copy status to BORROWED
        copy.setAvailabilityStatus(CopyStatus.BORROWED);
        bookCopyRepository.save(copy);

        BorrowRecord record = BorrowRecord.builder()
                .member(member)
                .bookCopy(copy)
                .librarian(librarian)
                .borrowDate(borrowDate)
                .dueDate(dueDate)
                .renewalCount(0)
                .status(BorrowStatus.ISSUED)
                .remarks(dto.getRemarks())
                .build();

        BorrowRecord saved = borrowRecordRepository.save(record);
        log.info("Issued copy {} of '{}' to member {} due on {}",
                copy.getBarcode(), copy.getBook().getTitle(), member.getMemberCode(), dueDate);

        return saved;
    }

    @Override
    public BorrowRecord renewLoan(Long borrowRecordId) {
        BorrowRecord record = borrowRecordRepository.findById(borrowRecordId)
                .orElseThrow(() -> new ResourceNotFoundException("Loan record not found with id: " + borrowRecordId));

        if (record.getStatus() != BorrowStatus.ISSUED) {
            throw new BusinessRuleViolationException("Cannot renew a book loan that is not currently active.");
        }

        int maxRenewals = record.getMember().getMembershipType().getMaxRenewals();
        if (record.getRenewalCount() >= maxRenewals) {
            throw new BusinessRuleViolationException("Maximum renewals limit (" + maxRenewals + ") reached for this loan.");
        }

        int durationDays = record.getMember().getMembershipType().getBorrowDurationDays();
        LocalDate newDueDate = record.getDueDate().isAfter(LocalDate.now()) ?
                record.getDueDate().plusDays(durationDays) : LocalDate.now().plusDays(durationDays);

        record.setDueDate(newDueDate);
        record.setRenewalCount(record.getRenewalCount() + 1);

        return borrowRecordRepository.save(record);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<BorrowRecord> findById(Long id) {
        return borrowRecordRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BorrowRecord> findActiveLoansByMember(Long memberId) {
        return borrowRecordRepository.findByMemberIdAndStatusIn(memberId, List.of(BorrowStatus.ISSUED, BorrowStatus.OVERDUE));
    }

    @Override
    @Transactional(readOnly = true)
    public Page<BorrowRecord> findLoanHistoryByMember(Long memberId, Pageable pageable) {
        return borrowRecordRepository.findByMemberIdOrderByBorrowDateDesc(memberId, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public List<BorrowRecord> findOverdueLoans() {
        return borrowRecordRepository.findOverdueLoans(LocalDate.now());
    }

    @Override
    @Transactional(readOnly = true)
    public long countActiveLoansByMember(Long memberId) {
        return borrowRecordRepository.countActiveLoansByMemberId(memberId);
    }

    @Override
    @Transactional(readOnly = true)
    public long countOverdueLoans() {
        return borrowRecordRepository.countOverdueLoans(LocalDate.now());
    }

    @Override
    @Transactional(readOnly = true)
    public long countLoansToday() {
        return borrowRecordRepository.countByBorrowDate(LocalDate.now());
    }
}
