package com.library.erp.repository;

import com.library.erp.entity.MembershipType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MembershipTypeRepository extends JpaRepository<MembershipType, Long> {
    Optional<MembershipType> findByName(String name);
    boolean existsByName(String name);
}
