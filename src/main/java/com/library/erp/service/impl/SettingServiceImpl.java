package com.library.erp.service.impl;

import com.library.erp.dto.setting.LibrarySettingDto;
import com.library.erp.entity.LibrarySetting;
import com.library.erp.repository.LibrarySettingRepository;
import com.library.erp.service.SettingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
@Transactional
public class SettingServiceImpl implements SettingService {

    private final LibrarySettingRepository settingRepository;

    @Override
    @Transactional(readOnly = true)
    public String getSettingValue(String key, String defaultValue) {
        return settingRepository.findBySettingKey(key)
                .map(LibrarySetting::getSettingValue)
                .orElse(defaultValue);
    }

    @Override
    @Transactional(readOnly = true)
    public int getSettingAsInt(String key, int defaultValue) {
        String val = getSettingValue(key, String.valueOf(defaultValue));
        try {
            return Integer.parseInt(val);
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    @Override
    @Transactional(readOnly = true)
    public BigDecimal getSettingAsDecimal(String key, BigDecimal defaultValue) {
        String val = getSettingValue(key, defaultValue != null ? defaultValue.toString() : "0.00");
        try {
            return new BigDecimal(val);
        } catch (Exception e) {
            return defaultValue;
        }
    }

    @Override
    public LibrarySetting saveSetting(LibrarySettingDto dto) {
        Optional<LibrarySetting> opt = settingRepository.findBySettingKey(dto.getSettingKey());
        LibrarySetting setting;
        if (opt.isPresent()) {
            setting = opt.get();
            setting.setSettingValue(dto.getSettingValue());
            if (dto.getDescription() != null) setting.setDescription(dto.getDescription());
        } else {
            setting = LibrarySetting.builder()
                    .settingKey(dto.getSettingKey())
                    .settingValue(dto.getSettingValue())
                    .category(dto.getCategory() != null ? dto.getCategory() : "GENERAL")
                    .description(dto.getDescription())
                    .build();
        }
        return settingRepository.save(setting);
    }

    @Override
    @Transactional(readOnly = true)
    public List<LibrarySetting> findAllSettings() {
        return settingRepository.findAll();
    }

    @Override
    public void seedDefaultSettingsIfEmpty() {
        if (settingRepository.count() == 0) {
            log.info("Seeding default ERP settings...");
            saveSetting(new LibrarySettingDto(null, "circulation.default_fine_rate", "10.00", "CIRCULATION", "Daily overdue fine amount (₹)"));
            saveSetting(new LibrarySettingDto(null, "circulation.grace_period_days", "1", "CIRCULATION", "Days grace period before fine starts calculating"));
            saveSetting(new LibrarySettingDto(null, "circulation.lost_book_multiplier", "2.0", "CIRCULATION", "Replacement fine multiplier for lost books"));
            saveSetting(new LibrarySettingDto(null, "reservation.hold_period_days", "3", "RESERVATION", "Days a reserved book is kept on hold before expiring"));
            saveSetting(new LibrarySettingDto(null, "general.library_name", "SmartLibrary Enterprise", "GENERAL", "Official library institution name"));
            saveSetting(new LibrarySettingDto(null, "general.operating_hours", "08:00 AM - 09:00 PM", "GENERAL", "Daily library operating hours"));
        }
    }
}
