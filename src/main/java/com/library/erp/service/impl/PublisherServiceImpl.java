package com.library.erp.service.impl;

import com.library.erp.dto.catalog.PublisherDto;
import com.library.erp.entity.Publisher;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.PublisherRepository;
import com.library.erp.service.PublisherService;
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
public class PublisherServiceImpl implements PublisherService {

    private final PublisherRepository publisherRepository;

    @Override
    public Publisher createPublisher(PublisherDto dto) {
        if (publisherRepository.existsByName(dto.getName().trim())) {
            throw new DuplicateResourceException("Publisher with name '" + dto.getName() + "' already exists.");
        }
        Publisher publisher = Publisher.builder()
                .name(dto.getName().trim())
                .address(dto.getAddress())
                .contactEmail(dto.getContactEmail())
                .phone(dto.getPhone())
                .website(dto.getWebsite())
                .build();
        return publisherRepository.save(publisher);
    }

    @Override
    public Publisher updatePublisher(Long id, PublisherDto dto) {
        Publisher publisher = publisherRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Publisher not found with id: " + id));

        publisher.setName(dto.getName().trim());
        publisher.setAddress(dto.getAddress());
        publisher.setContactEmail(dto.getContactEmail());
        publisher.setPhone(dto.getPhone());
        publisher.setWebsite(dto.getWebsite());

        return publisherRepository.save(publisher);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Publisher> findById(Long id) {
        return publisherRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Publisher> findAllPublishers() {
        return publisherRepository.findByOrderByNameAsc();
    }

    @Override
    @Transactional(readOnly = true)
    public Page<Publisher> searchPublishers(String name, Pageable pageable) {
        if (name == null || name.trim().isEmpty()) {
            return publisherRepository.findAll(pageable);
        }
        return publisherRepository.findByNameContainingIgnoreCase(name.trim(), pageable);
    }

    @Override
    public void deletePublisher(Long id) {
        if (!publisherRepository.existsById(id)) {
            throw new ResourceNotFoundException("Publisher not found with id: " + id);
        }
        publisherRepository.deleteById(id);
    }
}
