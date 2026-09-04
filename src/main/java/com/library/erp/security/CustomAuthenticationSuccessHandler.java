package com.library.erp.security;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Collection;

/**
 * Directs the authenticated user to their role-specific dashboard.
 * - ROLE_ADMIN -> /admin/dashboard
 * - ROLE_LIBRARIAN -> /librarian/dashboard
 * - ROLE_MEMBER -> /member/dashboard
 */
@Component
public class CustomAuthenticationSuccessHandler implements AuthenticationSuccessHandler {

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication) throws IOException, ServletException {
        Collection<? extends GrantedAuthority> authorities = authentication.getAuthorities();

        for (GrantedAuthority authority : authorities) {
            String role = authority.getAuthority();
            if ("ROLE_ADMIN".equals(role)) {
                response.sendRedirect(request.getContextPath() + "/admin/dashboard");
                return;
            } else if ("ROLE_LIBRARIAN".equals(role)) {
                response.sendRedirect(request.getContextPath() + "/librarian/dashboard");
                return;
            } else if ("ROLE_MEMBER".equals(role)) {
                response.sendRedirect(request.getContextPath() + "/member/dashboard");
                return;
            }
        }

        // Default fallback if no known role matches
        response.sendRedirect(request.getContextPath() + "/");
    }
}
