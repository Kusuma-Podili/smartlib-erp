package com.library.erp.service;

import com.library.erp.entity.User;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.entity.enums.UserStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

public interface UserService {
    User createUser(User user, RoleName roleName);
    Optional<User> findById(Long id);
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    Page<User> findAllUsers(Pageable pageable);
    Page<User> findUsersByRole(RoleName roleName, Pageable pageable);
    User updateUserStatus(Long userId, UserStatus status);
    User updateProfile(Long userId, String firstName, String lastName, String phone);
    boolean existsByUsername(String username);
    boolean existsByEmail(String email);
    long countTotalUsers();
    long countUsersByRole(RoleName roleName);
    long countUsersByStatus(UserStatus status);
}
