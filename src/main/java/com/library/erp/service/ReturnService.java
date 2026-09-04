package com.library.erp.service;

import com.library.erp.dto.circulation.ReturnProcessDto;
import com.library.erp.entity.Librarian;
import com.library.erp.entity.ReturnRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

public interface ReturnService {
    ReturnRecord processReturn(ReturnProcessDto dto, Librarian librarian);
    Optional<ReturnRecord> findById(Long id);
    Page<ReturnRecord> findAllReturns(Pageable pageable);
    long countReturnsToday();
}
