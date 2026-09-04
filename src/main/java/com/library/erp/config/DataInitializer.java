package com.library.erp.config;

import com.library.erp.entity.Role;
import com.library.erp.entity.User;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.entity.enums.UserStatus;
import com.library.erp.repository.RoleRepository;
import com.library.erp.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.Set;

/**
 * Initializes essential seed data: Roles and default credentials for test / startup.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final RoleRepository roleRepository;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final com.library.erp.service.MembershipTypeService membershipTypeService;
    private final com.library.erp.service.SettingService settingService;

    @Override
    @Transactional
    public void run(String... args) {
        log.info("Checking database initialization for SmartLibrary ERP...");

        Role adminRole = createRoleIfNotFound(RoleName.ROLE_ADMIN, "System Administrator with full access");
        Role librarianRole = createRoleIfNotFound(RoleName.ROLE_LIBRARIAN, "Librarian staff with circulation permissions");
        Role memberRole = createRoleIfNotFound(RoleName.ROLE_MEMBER, "Library patron with search and borrow access");

        createUserIfNotFound("admin", "admin@library.com", "Admin@123", "System", "Administrator", "9876543210", adminRole);
        createUserIfNotFound("librarian", "librarian@library.com", "Librarian@123", "Chief", "Librarian", "9876543211", librarianRole);
        createUserIfNotFound("member", "member@library.com", "Member@123", "John", "Doe", "9876543212", memberRole);

        membershipTypeService.seedDefaultMembershipTypesIfEmpty();
        settingService.seedDefaultSettingsIfEmpty();

        log.info("SmartLibrary ERP seed data initialization complete.");
    }

    private Role createRoleIfNotFound(RoleName roleName, String description) {
        return roleRepository.findByName(roleName).orElseGet(() -> {
            log.info("Creating system role: {}", roleName);
            Role role = Role.builder()
                    .name(roleName)
                    .description(description)
                    .build();
            return roleRepository.save(role);
        });
    }

    private void createUserIfNotFound(String username, String email, String rawPassword,
                                      String firstName, String lastName, String phone, Role role) {
        if (!userRepository.existsByUsername(username) && !userRepository.existsByEmail(email)) {
            log.info("Creating default seed user: {} ({}) with role {}", username, email, role.getName());
            User user = User.builder()
                    .username(username)
                    .email(email)
                    .password(passwordEncoder.encode(rawPassword))
                    .firstName(firstName)
                    .lastName(lastName)
                    .phone(phone)
                    .status(UserStatus.ACTIVE)
                    .roles(Set.of(role))
                    .build();
            userRepository.save(user);
        }
    }
}
