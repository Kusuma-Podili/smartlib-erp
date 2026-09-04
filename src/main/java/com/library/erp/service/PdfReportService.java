package com.library.erp.service;

import com.library.erp.entity.Book;
import com.library.erp.entity.BorrowRecord;
import com.library.erp.repository.BookRepository;
import com.library.erp.repository.BorrowRecordRepository;
import com.lowagie.text.*;
import com.lowagie.text.pdf.PdfPCell;
import com.lowagie.text.pdf.PdfPTable;
import com.lowagie.text.pdf.PdfWriter;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.awt.Color;
import java.io.OutputStream;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class PdfReportService {

    private final BookRepository bookRepository;
    private final BorrowRecordRepository borrowRecordRepository;

    public void generateBookCatalogPdf(OutputStream out) throws DocumentException {
        Document document = new Document(PageSize.A4.rotate());
        PdfWriter.getInstance(document, out);
        document.open();

        Font titleFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 18, new Color(15, 23, 42));
        Paragraph title = new Paragraph("SmartLibrary ERP - Complete Books Catalog", titleFont);
        title.setAlignment(Element.ALIGN_CENTER);
        document.add(title);

        Paragraph timestamp = new Paragraph("Generated on: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")),
                FontFactory.getFont(FontFactory.HELVETICA, 10, Color.GRAY));
        timestamp.setAlignment(Element.ALIGN_CENTER);
        timestamp.setSpacingAfter(15);
        document.add(timestamp);

        PdfPTable table = new PdfPTable(7);
        table.setWidthPercentage(100);
        table.setWidths(new float[]{3f, 5f, 4f, 3f, 2f, 2f, 2f});

        addTableHeader(table, "ISBN", "Title", "Author(s)", "Category", "Copies", "Avail", "Status");

        List<Book> books = bookRepository.findAll();
        for (Book b : books) {
            table.addCell(b.getIsbn());
            table.addCell(b.getTitle());
            table.addCell(b.getAuthorsFormatted());
            table.addCell(b.getCategory() != null ? b.getCategory().getName() : "-");
            table.addCell(String.valueOf(b.getTotalCopiesCount()));
            table.addCell(String.valueOf(b.getAvailableCopiesCount()));
            table.addCell(b.getStatus().name());
        }

        document.add(table);
        document.close();
    }

    public void generateLoansSummaryPdf(OutputStream out) throws DocumentException {
        Document document = new Document(PageSize.A4.rotate());
        PdfWriter.getInstance(document, out);
        document.open();

        Font titleFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 18, new Color(15, 23, 42));
        Paragraph title = new Paragraph("SmartLibrary ERP - Circulation & Loans Statement", titleFont);
        title.setAlignment(Element.ALIGN_CENTER);
        document.add(title);

        Paragraph timestamp = new Paragraph("Generated on: " + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")),
                FontFactory.getFont(FontFactory.HELVETICA, 10, Color.GRAY));
        timestamp.setAlignment(Element.ALIGN_CENTER);
        timestamp.setSpacingAfter(15);
        document.add(timestamp);

        PdfPTable table = new PdfPTable(7);
        table.setWidthPercentage(100);
        table.setWidths(new float[]{1.5f, 3f, 4f, 4f, 2.5f, 2.5f, 2f});

        addTableHeader(table, "ID", "Member ID", "Patron Name", "Book Title", "Borrowed", "Due Date", "Status");

        List<BorrowRecord> loans = borrowRecordRepository.findAll();
        for (BorrowRecord l : loans) {
            table.addCell(String.valueOf(l.getId()));
            table.addCell(l.getMember().getMemberCode());
            table.addCell(l.getMember().getUser().getFullName());
            table.addCell(l.getBookCopy().getBook().getTitle());
            table.addCell(l.getBorrowDate().toString());
            table.addCell(l.getDueDate().toString());
            table.addCell(l.getStatus().name());
        }

        document.add(table);
        document.close();
    }

    private void addTableHeader(PdfPTable table, String... headers) {
        Font headerFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 11, Color.WHITE);
        Color headerBg = new Color(30, 58, 138);

        for (String h : headers) {
            PdfPCell cell = new PdfPCell(new Phrase(h, headerFont));
            cell.setBackgroundColor(headerBg);
            cell.setPadding(6);
            cell.setHorizontalAlignment(Element.ALIGN_CENTER);
            table.addCell(cell);
        }
    }
}
