package com.library.erp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "librarians")
public class Librarian extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private User user;

    @Column(name = "employee_code", nullable = false, unique = true, length = 40)
    private String employeeCode;

    @Column(name = "department", length = 80)
    @Builder.Default
    private String department = "Circulation & Archiving";

    @Column(name = "qualification", length = 100)
    private String qualification;

    @Column(name = "joining_date")
    @Builder.Default
    private LocalDate joiningDate = LocalDate.now();
}
