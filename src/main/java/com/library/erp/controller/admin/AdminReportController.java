package com.library.erp.controller.admin;

import com.library.erp.service.CsvExportService;
import com.library.erp.service.PdfReportService;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.IOException;
import java.io.PrintWriter;

@Controller
@RequestMapping("/admin/reports")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class AdminReportController {

    private final CsvExportService csvExportService;
    private final PdfReportService pdfReportService;

    @GetMapping
    public String reportsDashboard(Model model) {
        model.addAttribute("activeMenu", "admin-reports");
        return "admin/reports/index";
    }

    @GetMapping("/books/csv")
    public void downloadBooksCsv(HttpServletResponse response) throws IOException {
        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=\"books_catalog.csv\"");
        PrintWriter writer = response.getWriter();
        csvExportService.exportBooksCsv(writer);
        writer.flush();
    }

    @GetMapping("/members/csv")
    public void downloadMembersCsv(HttpServletResponse response) throws IOException {
        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=\"members_registry.csv\"");
        PrintWriter writer = response.getWriter();
        csvExportService.exportMembersCsv(writer);
        writer.flush();
    }

    @GetMapping("/loans/csv")
    public void downloadLoansCsv(HttpServletResponse response) throws IOException {
        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=\"loans_history.csv\"");
        PrintWriter writer = response.getWriter();
        csvExportService.exportBorrowRecordsCsv(writer);
        writer.flush();
    }

    @GetMapping("/fines/csv")
    public void downloadFinesCsv(HttpServletResponse response) throws IOException {
        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=\"fines_revenue.csv\"");
        PrintWriter writer = response.getWriter();
        csvExportService.exportFinesCsv(writer);
        writer.flush();
    }

    @GetMapping("/books/pdf")
    public void downloadBooksPdf(HttpServletResponse response) throws Exception {
        response.setContentType("application/pdf");
        response.setHeader("Content-Disposition", "attachment; filename=\"books_catalog.pdf\"");
        pdfReportService.generateBookCatalogPdf(response.getOutputStream());
        response.getOutputStream().flush();
    }

    @GetMapping("/loans/pdf")
    public void downloadLoansPdf(HttpServletResponse response) throws Exception {
        response.setContentType("application/pdf");
        response.setHeader("Content-Disposition", "attachment; filename=\"loans_statement.pdf\"");
        pdfReportService.generateLoansSummaryPdf(response.getOutputStream());
        response.getOutputStream().flush();
    }
}
