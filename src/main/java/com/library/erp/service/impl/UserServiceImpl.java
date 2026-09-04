package com.library.erp.service.impl;

import com.library.erp.entity.Role;
import com.library.erp.entity.User;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.entity.enums.UserStatus;
import com.library.erp.exception.DuplicateResourceException;
import com.library.erp.exception.ResourceNotFoundException;
import com.library.erp.repository.RoleRepository;
import com.library.erp.repository.UserRepository;
import com.library.erp.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public User createUser(User user, RoleName roleName) {
        if (userRepository.existsByUsername(user.getUsername())) {
            throw new DuplicateResourceException("Username '" + user.getUsername() + "' is already taken.");
        }
        if (userRepository.existsByEmail(user.getEmail())) {
            throw new DuplicateResourceException("Email '" + user.getEmail() + "' is already registered.");
        }

        Role role = roleRepository.findByName(roleName)
                .orElseThrow(() -> new ResourceNotFoundException("Role not found: " + roleName));

        user.setPassword(passwordEncoder.encode(user.getPassword()));
        user.getRoles().add(role);
        user.setStatus(UserStatus.ACTIVE);

        return userRepository.save(user);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<User> findAllUsers(Pageable pageable) {
        return userRepository.findAll(pageable);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<User> findUsersByRole(RoleName roleName, Pageable pageable) {
        return userRepository.findAllByRoleName(roleName, pageable);
    }

    @Override
    public User updateUserStatus(Long userId, UserStatus status) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        user.setStatus(status);
        return userRepository.save(user);
    }

    @Override
    public User updateProfile(Long userId, String firstName, String lastName, String phone) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + userId));
        user.setFirstName(firstName);
        user.setLastName(lastName);
        user.setPhone(phone);
        return userRepository.save(user);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean existsByUsername(String username) {
        return userRepository.existsByUsername(username);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }

    @Override
    @Transactional(readOnly = true)
    public long countTotalUsers() {
        return userRepository.count();
    }

    @Override
    @Transactional(readOnly = true)
    public long countUsersByRole(RoleName roleName) {
        return userRepository.countByRoleName(roleName);
    }

    @Override
    @Transactional(readOnly = true)
    public long countUsersByStatus(UserStatus status) {
        return userRepository.countByStatus(status);
    }
}
