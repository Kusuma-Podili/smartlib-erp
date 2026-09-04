package com.library.erp.service;

import com.library.erp.dto.catalog.AuthorDto;
import com.library.erp.entity.Author;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

public interface AuthorService {
    Author createAuthor(AuthorDto dto);
    Author updateAuthor(Long id, AuthorDto dto);
    Optional<Author> findById(Long id);
    List<Author> findAllAuthors();
    Page<Author> searchAuthors(String query, Pageable pageable);
    void deleteAuthor(Long id);
}
