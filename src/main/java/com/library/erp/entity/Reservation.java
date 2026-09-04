package com.library.erp.entity;

import com.library.erp.entity.enums.ReservationStatus;
import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "reservations", indexes = {
        @Index(name = "idx_res_status", columnList = "status"),
        @Index(name = "idx_res_queue", columnList = "queue_position")
})
public class Reservation extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "member_id", nullable = false)
    private Member member;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    @Column(name = "reservation_date", nullable = false)
    @Builder.Default
    private LocalDateTime reservationDate = LocalDateTime.now();

    @Column(name = "queue_position", nullable = false)
    private Integer queuePosition;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    @Builder.Default
    private ReservationStatus status = ReservationStatus.PENDING;

    @Column(name = "hold_expiry_date")
    private LocalDateTime holdExpiryDate;

    @Column(name = "remarks", length = 255)
    private String remarks;

    public boolean isPending() {
        return this.status == ReservationStatus.PENDING || this.status == ReservationStatus.NOTIFIED;
    }
}
