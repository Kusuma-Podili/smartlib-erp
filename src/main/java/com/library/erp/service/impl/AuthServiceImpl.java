package com.library.erp.service.impl;

import com.library.erp.dto.auth.RegisterRequestDto;
import com.library.erp.entity.User;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.UserRepository;
import com.library.erp.service.AuthService;
import com.library.erp.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserService userService;
    private final UserRepository userRepository;

    @Override
    @Transactional
    public User registerMember(RegisterRequestDto dto) {
        if (!dto.getPassword().equals(dto.getConfirmPassword())) {
            throw new BusinessRuleViolationException("Password and Confirm Password do not match.");
        }

        User user = User.builder()
                .username(dto.getUsername().trim().toLowerCase())
                .email(dto.getEmail().trim().toLowerCase())
                .password(dto.getPassword())
                .firstName(dto.getFirstName().trim())
                .lastName(dto.getLastName().trim())
                .phone(dto.getPhone() != null ? dto.getPhone().trim() : null)
                .build();

        return userService.createUser(user, RoleName.ROLE_MEMBER);
    }

    @Override
    @Transactional(readOnly = true)
    public User getCurrentAuthenticatedUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated() || "anonymousUser".equals(authentication.getPrincipal())) {
            throw new ResourceNotFoundException("No authenticated user found in session.");
        }
        String username = authentication.getName();
        return userRepository.findByUsernameOrEmail(username)
                .orElseThrow(() -> new ResourceNotFoundException("Authenticated user not found in database: " + username));
    }
}
