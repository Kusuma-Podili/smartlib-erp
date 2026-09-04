package com.library.erp.dto.member;

import jakarta.validation.constraints.*;
import lombok.*;

import java.math.BigDecimal;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MembershipTypeDto {
    private Long id;

    @NotBlank(message = "Tier name is required")
    private String name;

    @Min(value = 1, message = "Borrowing limit must be at least 1 book")
    @Max(value = 50, message = "Borrowing limit cannot exceed 50 books")
    private Integer borrowingLimit;

    @Min(value = 1, message = "Borrow duration must be at least 1 day")
    private Integer borrowDurationDays;

    @PositiveOrZero
    private Integer gracePeriodDays;

    @PositiveOrZero
    private Integer maxRenewals;

    @PositiveOrZero
    private BigDecimal finePerDay;

    @PositiveOrZero
    private BigDecimal annualFee;

    private String description;
}
