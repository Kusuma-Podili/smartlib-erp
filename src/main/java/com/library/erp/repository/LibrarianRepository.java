package com.library.erp.repository;

import com.library.erp.entity.Librarian;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface LibrarianRepository extends JpaRepository<Librarian, Long> {
    Optional<Librarian> findByEmployeeCode(String employeeCode);
    Optional<Librarian> findByUserId(Long userId);
    Optional<Librarian> findByUserUsername(String username);
    boolean existsByEmployeeCode(String employeeCode);
}
