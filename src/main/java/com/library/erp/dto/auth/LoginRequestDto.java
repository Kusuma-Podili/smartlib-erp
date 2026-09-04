package com.library.erp.dto.auth;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

/**
 * Data transfer object for login credentials.
 */
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoginRequestDto {

    @NotBlank(message = "Username or email is required")
    private String username;

    @NotBlank(message = "Password is required")
    private String password;
}
