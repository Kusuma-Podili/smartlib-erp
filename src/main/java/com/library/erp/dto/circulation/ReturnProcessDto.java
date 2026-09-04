package com.library.erp.dto.circulation;

import com.library.erp.entity.enums.CopyCondition;
import jakarta.validation.constraints.NotBlank;
import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ReturnProcessDto {

    @NotBlank(message = "Book copy barcode is required")
    private String barcode;

    @Builder.Default
    private CopyCondition condition = CopyCondition.GOOD;

    private BigDecimal additionalDamageCharge;

    private String remarks;
}
