package com.library.erp.repository;

import com.library.erp.entity.Reservation;
import com.library.erp.entity.enums.ReservationStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ReservationRepository extends JpaRepository<Reservation, Long> {

    @Query("SELECT r FROM Reservation r WHERE r.member.id = :memberId AND r.book.id = :bookId AND r.status IN ('PENDING', 'NOTIFIED')")
    Optional<Reservation> findActiveReservation(@Param("memberId") Long memberId, @Param("bookId") Long bookId);

    List<Reservation> findByBookIdAndStatusOrderByQueuePositionAsc(Long bookId, ReservationStatus status);

    @Query("SELECT MAX(r.queuePosition) FROM Reservation r WHERE r.book.id = :bookId AND r.status IN ('PENDING', 'NOTIFIED')")
    Integer findMaxQueuePositionByBookId(@Param("bookId") Long bookId);

    Page<Reservation> findByMemberIdOrderByReservationDateDesc(Long memberId, Pageable pageable);

    @Query("SELECT COUNT(r) FROM Reservation r WHERE r.member.id = :memberId AND r.status IN ('PENDING', 'NOTIFIED')")
    long countActiveReservationsByMemberId(@Param("memberId") Long memberId);

    long countByStatus(ReservationStatus status);
}
