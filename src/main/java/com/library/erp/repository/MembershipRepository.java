package com.library.erp.repository;

import com.library.erp.entity.Membership;
import com.library.erp.entity.enums.MembershipStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface MembershipRepository extends JpaRepository<Membership, Long> {

    List<Membership> findByMemberIdOrderByStartDateDesc(Long memberId);

    Optional<Membership> findFirstByMemberIdAndStatusOrderByExpiryDateDesc(Long memberId, MembershipStatus status);

    @Query("SELECT m FROM Membership m WHERE m.status = 'ACTIVE' AND m.expiryDate < :currentDate")
    List<Membership> findExpiredMemberships(@Param("currentDate") LocalDate currentDate);

    long countByStatus(MembershipStatus status);
}
