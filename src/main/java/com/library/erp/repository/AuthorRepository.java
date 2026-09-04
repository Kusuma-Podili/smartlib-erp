package com.library.erp.repository;

import com.library.erp.entity.Author;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AuthorRepository extends JpaRepository<Author, Long> {
    List<Author> findByOrderByLastNameAscFirstNameAsc();

    @Query("SELECT a FROM Author a WHERE LOWER(a.firstName) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(a.lastName) LIKE LOWER(CONCAT('%', :query, '%'))")
    Page<Author> searchAuthors(@Param("query") String query, Pageable pageable);
}
