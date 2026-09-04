package com.library.erp.dto.member;

import jakarta.validation.constraints.*;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MemberRegistrationDto {

    @NotBlank(message = "Username is mandatory")
    @Size(min = 4, max = 30)
    private String username;

    @NotBlank(message = "Email is mandatory")
    @Email
    private String email;

    @NotBlank(message = "First name is mandatory")
    private String firstName;

    @NotBlank(message = "Last name is mandatory")
    private String lastName;

    private String password;

    @Pattern(regexp = "^[0-9]{10,15}$", message = "Phone number must be valid 10 digits")
    private String phone;

    @NotNull(message = "Please select a membership tier")
    private Long membershipTypeId;

    private String address;

    private LocalDate dateOfBirth;

    private String occupation;

    private String identityProofType;

    private String identityProofNumber;
}
