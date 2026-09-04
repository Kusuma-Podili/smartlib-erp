package com.library.erp.dto.circulation;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BorrowRequestDto {

    @NotBlank(message = "Member code is required")
    private String memberCode;

    @NotBlank(message = "Book copy barcode is required")
    private String barcode;

    private String remarks;
}
