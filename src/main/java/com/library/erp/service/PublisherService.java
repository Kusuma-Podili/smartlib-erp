package com.library.erp.service;

import com.library.erp.dto.catalog.PublisherDto;
import com.library.erp.entity.Publisher;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

public interface PublisherService {
    Publisher createPublisher(PublisherDto dto);
    Publisher updatePublisher(Long id, PublisherDto dto);
    Optional<Publisher> findById(Long id);
    List<Publisher> findAllPublishers();
    Page<Publisher> searchPublishers(String name, Pageable pageable);
    void deletePublisher(Long id);
}
