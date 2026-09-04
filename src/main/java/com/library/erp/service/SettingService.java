package com.library.erp.service;

import com.library.erp.dto.setting.LibrarySettingDto;
import com.library.erp.entity.LibrarySetting;

import java.math.BigDecimal;
import java.util.List;

public interface SettingService {
    String getSettingValue(String key, String defaultValue);
    int getSettingAsInt(String key, int defaultValue);
    BigDecimal getSettingAsDecimal(String key, BigDecimal defaultValue);
    LibrarySetting saveSetting(LibrarySettingDto dto);
    List<LibrarySetting> findAllSettings();
    void seedDefaultSettingsIfEmpty();
}
