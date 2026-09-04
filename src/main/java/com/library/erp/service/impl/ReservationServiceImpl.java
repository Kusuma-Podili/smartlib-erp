package com.library.erp.service.impl;

import com.library.erp.entity.Book;
import com.library.erp.entity.Member;
import com.library.erp.entity.Reservation;
import com.library.erp.entity.enums.ReservationStatus;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.BookRepository;
import com.library.erp.repository.MemberRepository;
import com.library.erp.repository.ReservationRepository;
import com.library.erp.service.ReservationService;
import com.library.erp.service.SettingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class ReservationServiceImpl implements ReservationService {

    private final ReservationRepository reservationRepository;
    private final MemberRepository memberRepository;
    private final BookRepository bookRepository;
    private final SettingService settingService;

    @Override
    public Reservation reserveBook(Long memberId, Long bookId, String remarks) {
        Member member = memberRepository.findById(memberId)
                .orElseThrow(() -> new ResourceNotFoundException("Member not found with id: " + memberId));

        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + bookId));

        // Business Rule 4: Prevent duplicate active reservations for the same member and book
        Optional<Reservation> existing = reservationRepository.findActiveReservation(memberId, bookId);
        if (existing.isPresent()) {
            throw new BusinessRuleViolationException(
                    "You already have an active hold on this book (Current queue position: #" + existing.get().getQueuePosition() + ")."
            );
        }

        Integer maxQueue = reservationRepository.findMaxQueuePositionByBookId(bookId);
        int queuePosition = (maxQueue != null ? maxQueue : 0) + 1;

        Reservation reservation = Reservation.builder()
                .member(member)
                .book(book)
                .reservationDate(LocalDateTime.now())
                .queuePosition(queuePosition)
                .status(ReservationStatus.PENDING)
                .remarks(remarks)
                .build();

        Reservation saved = reservationRepository.save(reservation);
        log.info("Created reservation for member {} on book '{}' at queue position #{}",
                member.getMemberCode(), book.getTitle(), queuePosition);

        return saved;
    }

    @Override
    public Optional<Reservation> notifyNextInQueue(Long bookId) {
        List<Reservation> queue = reservationRepository.findByBookIdAndStatusOrderByQueuePositionAsc(
                bookId, ReservationStatus.PENDING
        );

        if (queue.isEmpty()) {
            return Optional.empty();
        }

        Reservation nextMember = queue.get(0);
        int holdDays = settingService.getSettingAsInt("reservation.hold_period_days", 3);

        nextMember.setStatus(ReservationStatus.NOTIFIED);
        nextMember.setHoldExpiryDate(LocalDateTime.now().plusDays(holdDays));
        reservationRepository.save(nextMember);

        log.info("Notified member {} for reserved book '{}' (Hold valid until {})",
                nextMember.getMember().getMemberCode(), nextMember.getBook().getTitle(), nextMember.getHoldExpiryDate());

        return Optional.of(nextMember);
    }

    @Override
    public Reservation cancelReservation(Long reservationId, Long memberId) {
        Reservation reservation = reservationRepository.findById(reservationId)
                .orElseThrow(() -> new ResourceNotFoundException("Reservation not found with id: " + reservationId));

        if (memberId != null && !reservation.getMember().getId().equals(memberId)) {
            throw new BusinessRuleViolationException("You cannot cancel another member's reservation.");
        }

        reservation.setStatus(ReservationStatus.CANCELLED);
        return reservationRepository.save(reservation);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Reservation> findReservationsByMember(Long memberId, Pageable pageable) {
        return reservationRepository.findByMemberIdOrderByReservationDateDesc(memberId, pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public long countActiveReservationsByMember(Long memberId) {
        return reservationRepository.countActiveReservationsByMemberId(memberId);
    }

    @Override
    @Transactional(readOnly = true)
    public long countPendingReservations() {
        return reservationRepository.countByStatus(ReservationStatus.PENDING);
    }
}
