package com.library.erp.dto.circulation;

import com.library.erp.entity.enums.PaymentMethod;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class FinePaymentDto {

    @NotNull(message = "Fine ID is required")
    private Long fineId;

    @NotNull(message = "Payment amount is required")
    @Positive(message = "Payment amount must be positive")
    private BigDecimal amountPaid;

    @Builder.Default
    private PaymentMethod paymentMethod = PaymentMethod.CASH;

    private String transactionReference;

    private String remarks;
}
