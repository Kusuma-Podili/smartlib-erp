package com.library.erp.dto.catalog;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PublisherDto {
    private Long id;

    @NotBlank(message = "Publisher name is required")
    private String name;

    private String address;
    private String contactEmail;
    private String phone;
    private String website;
    private int bookCount;
}
