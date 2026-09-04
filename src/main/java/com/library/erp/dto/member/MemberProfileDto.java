package com.library.erp.dto.member;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MemberProfileDto {
    private Long id;
    private Long userId;
    private String memberCode;
    private String username;
    private String email;

    @NotBlank(message = "First name is mandatory")
    private String firstName;

    @NotBlank(message = "Last name is mandatory")
    private String lastName;

    private String phone;
    private String address;
    private LocalDate dateOfBirth;
    private String occupation;
    private String membershipTypeName;
    private LocalDate membershipExpiryDate;
    private boolean membershipActive;
}
