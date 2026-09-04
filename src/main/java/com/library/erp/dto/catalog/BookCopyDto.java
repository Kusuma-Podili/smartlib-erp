package com.library.erp.dto.catalog;

import com.library.erp.entity.enums.CopyCondition;
import com.library.erp.entity.enums.CopyStatus;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BookCopyDto {
    private Long id;
    private Long bookId;
    private String bookTitle;
    private String barcode;
    private Integer copyNumber;
    private CopyCondition conditionStatus;
    private CopyStatus availabilityStatus;
    private LocalDate acquiredDate;
    private String remarks;
}
