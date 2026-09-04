package com.library.erp.repository;

import com.library.erp.entity.Member;
import com.library.erp.entity.enums.UserStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MemberRepository extends JpaRepository<Member, Long>, JpaSpecificationExecutor<Member> {

    Optional<Member> findByMemberCode(String memberCode);

    Optional<Member> findByUserId(Long userId);

    Optional<Member> findByUserUsername(String username);

    Optional<Member> findByUserEmail(String email);

    boolean existsByMemberCode(String memberCode);

    @Query("SELECT COUNT(m) FROM Member m WHERE m.user.status = :status")
    long countByStatus(@Param("status") UserStatus status);

    @Query("SELECT m FROM Member m WHERE LOWER(m.memberCode) LIKE LOWER(CONCAT('%', :query, '%')) " +
           "OR LOWER(m.user.firstName) LIKE LOWER(CONCAT('%', :query, '%')) " +
           "OR LOWER(m.user.lastName) LIKE LOWER(CONCAT('%', :query, '%')) " +
           "OR LOWER(m.user.email) LIKE LOWER(CONCAT('%', :query, '%'))")
    Page<Member> searchMembers(@Param("query") String query, Pageable pageable);
}
