package com.library.erp.service.impl;

import com.library.erp.dto.catalog.AuthorDto;
import com.library.erp.entity.Author;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.AuthorRepository;
import com.library.erp.service.AuthorService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class AuthorServiceImpl implements AuthorService {

    private final AuthorRepository authorRepository;

    @Override
    public Author createAuthor(AuthorDto dto) {
        Author author = Author.builder()
                .firstName(dto.getFirstName().trim())
                .lastName(dto.getLastName().trim())
                .biography(dto.getBiography())
                .email(dto.getEmail())
                .website(dto.getWebsite())
                .build();
        return authorRepository.save(author);
    }

    @Override
    public Author updateAuthor(Long id, AuthorDto dto) {
        Author author = authorRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Author not found with id: " + id));

        author.setFirstName(dto.getFirstName().trim());
        author.setLastName(dto.getLastName().trim());
        author.setBiography(dto.getBiography());
        author.setEmail(dto.getEmail());
        author.setWebsite(dto.getWebsite());

        return authorRepository.save(author);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Author> findById(Long id) {
        return authorRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Author> findAllAuthors() {
        return authorRepository.findByOrderByLastNameAscFirstNameAsc();
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Author> searchAuthors(String query, Pageable pageable) {
        if (query == null || query.trim().isEmpty()) {
            return authorRepository.findAll(pageable);
        }
        return authorRepository.searchAuthors(query.trim(), pageable);
    }

    @Override
    public void deleteAuthor(Long id) {
        if (!authorRepository.existsById(id)) {
            throw new ResourceNotFoundException("Author not found with id: " + id);
        }
        authorRepository.deleteById(id);
    }
}
