package com.library.erp.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Entity
@Table(name = "publishers")
public class Publisher extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false, unique = true, length = 100)
    private String name;

    @Column(name = "address", length = 255)
    private String address;

    @Column(name = "contact_email", length = 120)
    private String contactEmail;

    @Column(name = "phone", length = 20)
    private String phone;

    @Column(name = "website", length = 200)
    private String website;

    @OneToMany(mappedBy = "publisher", cascade = CascadeType.ALL)
    @Builder.Default
    private List<Book> books = new ArrayList<>();
}
