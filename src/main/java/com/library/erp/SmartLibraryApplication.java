package com.library.erp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * SmartLibrary ERP - Enterprise Library Management System
 * Built on Spring Boot 3, Spring Security 6, Spring Data JPA, and Thymeleaf.
 */
@SpringBootApplication
@EnableJpaAuditing
@EnableScheduling
@EnableAsync
public class SmartLibraryApplication {

    public static void main(String[] args) {
        SpringApplication.run(SmartLibraryApplication.class, args);
    }
}
