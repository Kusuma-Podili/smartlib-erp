package com.library.erp.dto.circulation;

import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ReservationDto {

    @NotNull(message = "Book ID is mandatory")
    private Long bookId;

    private String remarks;
}
