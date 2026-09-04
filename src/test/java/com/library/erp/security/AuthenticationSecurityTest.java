package com.library.erp.security;

import com.library.erp.entity.Role;
import com.library.erp.entity.User;
import com.library.erp.entity.enums.RoleName;
import com.library.erp.entity.enums.UserStatus;
import com.library.erp.repository.RoleRepository;
import com.library.erp.repository.UserRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrlPattern;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class AuthenticationSecurityTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RoleRepository roleRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private CustomAuthenticationSuccessHandler successHandler;

    @Test
    @DisplayName("Test 1: Unauthenticated user accessing protected admin route is redirected to login")
    void unauthenticatedAccessShouldRedirectToLogin() throws Exception {
        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrlPattern("**/login"));
    }

    @Test
    @DisplayName("Test 2: Passwords are encrypted with BCrypt and match original raw password")
    void passwordShouldBeHashedWithBcrypt() {
        String rawPassword = "SecurePassword@2026";
        String encoded = passwordEncoder.encode(rawPassword);

        assertThat(encoded).isNotEqualTo(rawPassword);
        assertThat(passwordEncoder.matches(rawPassword, encoded)).isTrue();
    }

    @Test
    @DisplayName("Test 3: Role-based redirect sends Admin, Librarian, and Member to respective dashboards")
    void roleBasedSuccessHandlerRedirectsCorrectly() throws Exception {
        MockHttpServletRequest request = new MockHttpServletRequest();
        MockHttpServletResponse response = new MockHttpServletResponse();

        // Admin Auth
        Authentication adminAuth = new UsernamePasswordAuthenticationToken("admin", "pass",
                List.of(new SimpleGrantedAuthority("ROLE_ADMIN")));
        successHandler.onAuthenticationSuccess(request, response, adminAuth);
        assertThat(response.getRedirectedUrl()).isEqualTo("/admin/dashboard");

        // Librarian Auth
        response = new MockHttpServletResponse();
        Authentication libAuth = new UsernamePasswordAuthenticationToken("librarian", "pass",
                List.of(new SimpleGrantedAuthority("ROLE_LIBRARIAN")));
        successHandler.onAuthenticationSuccess(request, response, libAuth);
        assertThat(response.getRedirectedUrl()).isEqualTo("/librarian/dashboard");

        // Member Auth
        response = new MockHttpServletResponse();
        Authentication memAuth = new UsernamePasswordAuthenticationToken("member", "pass",
                List.of(new SimpleGrantedAuthority("ROLE_MEMBER")));
        successHandler.onAuthenticationSuccess(request, response, memAuth);
        assertThat(response.getRedirectedUrl()).isEqualTo("/member/dashboard");
    }

    @Test
    @DisplayName("Test 4: User entity persistence and role association validation")
    void userCreationAndRoleVerification() {
        Role role = roleRepository.findByName(RoleName.ROLE_MEMBER).orElseGet(() ->
                roleRepository.save(Role.builder().name(RoleName.ROLE_MEMBER).description("Member role").build())
        );

        String username = "testuser_" + System.currentTimeMillis();
        User user = User.builder()
                .username(username)
                .email(username + "@test.com")
                .password(passwordEncoder.encode("Test@123"))
                .firstName("Test")
                .lastName("User")
                .status(UserStatus.ACTIVE)
                .roles(Set.of(role))
                .build();

        User saved = userRepository.save(user);
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.hasRole("ROLE_MEMBER")).isTrue();
        assertThat(saved.isActive()).isTrue();
    }

    @Test
    @org.springframework.security.test.context.support.WithMockUser(username = "admin", roles = {"ADMIN"})
    @DisplayName("Test 5: Admin dashboard view renders successfully without template errors")
    void adminDashboardRendersSuccessfully() throws Exception {
        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().isOk());
    }

    @Test
    @org.springframework.security.test.context.support.WithMockUser(username = "librarian", roles = {"LIBRARIAN"})
    @DisplayName("Test 6: Librarian dashboard view renders successfully")
    void librarianDashboardRendersSuccessfully() throws Exception {
        mockMvc.perform(get("/librarian/dashboard"))
                .andExpect(status().isOk());
    }

    @Test
    @org.springframework.security.test.context.support.WithMockUser(username = "member", roles = {"MEMBER"})
    @DisplayName("Test 7: Member dashboard view renders successfully")
    void memberDashboardRendersSuccessfully() throws Exception {
        mockMvc.perform(get("/member/dashboard"))
                .andExpect(status().isOk());
    }
}
