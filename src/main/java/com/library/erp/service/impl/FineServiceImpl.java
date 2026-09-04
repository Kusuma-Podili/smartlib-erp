package com.library.erp.service.impl;

import com.library.erp.dto.circulation.FinePaymentDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.FineStatus;
import com.library.erp.entity.enums.FineType;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.FinePaymentRepository;
import com.library.erp.repository.FineRepository;
import com.library.erp.service.FineService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.Year;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class FineServiceImpl implements FineService {

    private final FineRepository fineRepository;
    private final FinePaymentRepository finePaymentRepository;

    @Override
    public Fine createFine(BorrowRecord borrowRecord, Member member, FineType fineType, BigDecimal amount, String reason) {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            return null;
        }

        Fine fine = Fine.builder()
                .borrowRecord(borrowRecord)
                .member(member)
                .fineType(fineType)
                .amount(amount)
                .paidAmount(BigDecimal.ZERO)
                .status(FineStatus.UNPAID)
                .reason(reason)
                .build();

        Fine saved = fineRepository.save(fine);
        log.info("Assessed {} fine of ₹{} to member {}", fineType, amount, member.getMemberCode());
        return saved;
    }

    @Override
    public FinePayment recordPayment(FinePaymentDto dto, Librarian librarian) {
        Fine fine = fineRepository.findById(dto.getFineId())
                .orElseThrow(() -> new ResourceNotFoundException("Fine not found with id: " + dto.getFineId()));

        if (fine.getStatus() == FineStatus.PAID || fine.getStatus() == FineStatus.WAIVED) {
            throw new BusinessRuleViolationException("This fine has already been completely resolved.");
        }

        BigDecimal remainingBalance = fine.getOutstandingBalance();
        if (dto.getAmountPaid().compareTo(remainingBalance) > 0) {
            throw new BusinessRuleViolationException(
                    "Payment amount (₹" + dto.getAmountPaid() + ") exceeds outstanding balance (₹" + remainingBalance + ")."
            );
        }

        BigDecimal newPaidAmount = fine.getPaidAmount().add(dto.getAmountPaid());
        fine.setPaidAmount(newPaidAmount);

        if (newPaidAmount.compareTo(fine.getAmount()) >= 0) {
            fine.setStatus(FineStatus.PAID);
        } else {
            fine.setStatus(FineStatus.PARTIALLY_PAID);
        }
        fineRepository.save(fine);

        // Generate unique receipt number
        long count = finePaymentRepository.count() + 1;
        String receiptNumber = String.format("REC-%d-%05d", Year.now().getValue(), count);

        FinePayment payment = FinePayment.builder()
                .fine(fine)
                .member(fine.getMember())
                .librarian(librarian)
                .amountPaid(dto.getAmountPaid())
                .paymentDate(LocalDateTime.now())
                .paymentMethod(dto.getPaymentMethod())
                .receiptNumber(receiptNumber)
                .transactionReference(dto.getTransactionReference())
                .remarks(dto.getRemarks())
                .build();

        FinePayment savedPayment = finePaymentRepository.save(payment);
        log.info("Recorded fine payment of ₹{} with receipt {}", dto.getAmountPaid(), receiptNumber);

        return savedPayment;
    }

    @Override
    public Fine waiveFine(Long fineId, String reason) {
        Fine fine = fineRepository.findById(fineId)
                .orElseThrow(() -> new ResourceNotFoundException("Fine not found with id: " + fineId));

        fine.setStatus(FineStatus.WAIVED);
        fine.setReason((fine.getReason() != null ? fine.getReason() + " | " : "") + "Waived: " + reason);
        return fineRepository.save(fine);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Fine> findById(Long id) {
        return fineRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Fine> findUnpaidFinesByMember(Long memberId) {
        return fineRepository.findByMemberIdAndStatusIn(memberId, List.of(FineStatus.UNPAID, FineStatus.PARTIALLY_PAID));
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Fine> findFinesByMember(Long memberId, Pageable pageable) {
        return fineRepository.findByMemberIdOrderByCreatedAtDesc(memberId, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<FinePayment> findPaymentsByMember(Long memberId, Pageable pageable) {
        return finePaymentRepository.findByMemberIdOrderByPaymentDateDesc(memberId, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public BigDecimal getOutstandingBalanceForMember(Long memberId) {
        return fineRepository.calculateOutstandingBalanceByMemberId(memberId);
    }

    @Override
    @Transactional(readOnly = true)
    public BigDecimal getTotalUnpaidFines() {
        return fineRepository.calculateTotalUnpaidFines();
    }

    @Override
    @Transactional(readOnly = true)
    public BigDecimal getTotalCollectedFines() {
        return fineRepository.calculateTotalCollectedFines();
    }
}
