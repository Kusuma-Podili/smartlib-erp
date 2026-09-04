package com.library.erp.service;

import com.library.erp.entity.Reservation;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

public interface ReservationService {
    Reservation reserveBook(Long memberId, Long bookId, String remarks);
    Optional<Reservation> notifyNextInQueue(Long bookId);
    Reservation cancelReservation(Long reservationId, Long memberId);
    Page<Reservation> findReservationsByMember(Long memberId, Pageable pageable);
    long countActiveReservationsByMember(Long memberId);
    long countPendingReservations();
}
