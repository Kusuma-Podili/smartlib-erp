package com.library.erp.repository;

import com.library.erp.entity.LibrarySetting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface LibrarySettingRepository extends JpaRepository<LibrarySetting, Long> {
    Optional<LibrarySetting> findBySettingKey(String settingKey);
    boolean existsBySettingKey(String settingKey);
    List<LibrarySetting> findByCategoryOrderBySettingKeyAsc(String category);
}
