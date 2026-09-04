package com.library.erp.controller.admin;

import com.library.erp.dto.setting.LibrarySettingDto;
import com.library.erp.service.SettingService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/admin/settings")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminSettingsController {

    private final SettingService settingService;

    @GetMapping
    public String viewSettings(Model model) {
        model.addAttribute("settings", settingService.findAllSettings());
        model.addAttribute("activeMenu", "admin-settings");
        return "admin/settings/index";
    }

    @PostMapping("/update")
    public String updateSetting(@RequestParam("settingKey") String settingKey,
                                @RequestParam("settingValue") String settingValue,
                                RedirectAttributes redirectAttributes) {
        settingService.saveSetting(LibrarySettingDto.builder()
                .settingKey(settingKey)
                .settingValue(settingValue)
                .build());

        redirectAttributes.addFlashAttribute("successMessage", "Setting '" + settingKey + "' updated successfully.");
        return "redirect:/admin/settings";
    }
}
