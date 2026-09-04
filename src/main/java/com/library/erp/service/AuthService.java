package com.library.erp.service;

import com.library.erp.dto.auth.RegisterRequestDto;
import com.library.erp.entity.User;

public interface AuthService {
    User registerMember(RegisterRequestDto registerDto);
    User getCurrentAuthenticatedUser();
}
