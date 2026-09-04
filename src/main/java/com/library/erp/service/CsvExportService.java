package com.library.erp.service;

import com.library.erp.entity.Book;
import com.library.erp.entity.BorrowRecord;
import com.library.erp.entity.Fine;
import com.library.erp.entity.Member;
import com.library.erp.repository.BookRepository;
import com.library.erp.repository.BorrowRecordRepository;
import com.library.erp.repository.FineRepository;
import com.library.erp.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.PrintWriter;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CsvExportService {

    private final BookRepository bookRepository;
    private final MemberRepository memberRepository;
    private final BorrowRecordRepository borrowRecordRepository;
    private final FineRepository fineRepository;

    public void exportBooksCsv(PrintWriter writer) {
        writer.println("ISBN,Title,Category,Publisher,Authors,TotalCopies,AvailableCopies,ShelfLocation,Price,Status");
        List<Book> books = bookRepository.findAll();
        for (Book b : books) {
            writer.printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,\"%s\",%s,\"%s\"%n",
                    b.getIsbn(),
                    escapeCsv(b.getTitle()),
                    b.getCategory() != null ? escapeCsv(b.getCategory().getName()) : "",
                    b.getPublisher() != null ? escapeCsv(b.getPublisher().getName()) : "",
                    escapeCsv(b.getAuthorsFormatted()),
                    b.getTotalCopiesCount(),
                    b.getAvailableCopiesCount(),
                    (b.getShelfNumber() != null ? b.getShelfNumber() : "") + " / " + (b.getRackNumber() != null ? b.getRackNumber() : ""),
                    b.getPrice() != null ? b.getPrice().toString() : "0.00",
                    b.getStatus().name()
            );
        }
    }

    public void exportMembersCsv(PrintWriter writer) {
        writer.println("MemberCode,FullName,Username,Email,Phone,Tier,BorrowLimit,Status,JoinedDate");
        List<Member> members = memberRepository.findAll();
        for (Member m : members) {
            writer.printf("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,\"%s\",\"%s\"%n",
                    m.getMemberCode(),
                    escapeCsv(m.getUser().getFullName()),
                    m.getUser().getUsername(),
                    m.getUser().getEmail(),
                    m.getUser().getPhone() != null ? m.getUser().getPhone() : "",
                    m.getMembershipType().getName(),
                    m.getMembershipType().getBorrowingLimit(),
                    m.getUser().getStatus().name(),
                    m.getCreatedAt() != null ? m.getCreatedAt().toString() : ""
            );
        }
    }

    public void exportBorrowRecordsCsv(PrintWriter writer) {
        writer.println("LoanID,MemberCode,MemberName,BookTitle,Barcode,BorrowDate,DueDate,Status,RenewalCount");
        List<BorrowRecord> loans = borrowRecordRepository.findAll();
        for (BorrowRecord l : loans) {
            writer.printf("%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d%n",
                    l.getId(),
                    l.getMember().getMemberCode(),
                    escapeCsv(l.getMember().getUser().getFullName()),
                    escapeCsv(l.getBookCopy().getBook().getTitle()),
                    l.getBookCopy().getBarcode(),
                    l.getBorrowDate(),
                    l.getDueDate(),
                    l.getStatus().name(),
                    l.getRenewalCount()
            );
        }
    }

    public void exportFinesCsv(PrintWriter writer) {
        writer.println("FineID,MemberCode,MemberName,Type,Amount,PaidAmount,Balance,Status,Reason,Date");
        List<Fine> fines = fineRepository.findAll();
        for (Fine f : fines) {
            writer.printf("%d,\"%s\",\"%s\",\"%s\",%s,%s,%s,\"%s\",\"%s\",\"%s\"%n",
                    f.getId(),
                    f.getMember().getMemberCode(),
                    escapeCsv(f.getMember().getUser().getFullName()),
                    f.getFineType().name(),
                    f.getAmount(),
                    f.getPaidAmount(),
                    f.getOutstandingBalance(),
                    f.getStatus().name(),
                    escapeCsv(f.getReason() != null ? f.getReason() : ""),
                    f.getCreatedAt() != null ? f.getCreatedAt().toString() : ""
            );
        }
    }

    private String escapeCsv(String val) {
        if (val == null) return "";
        return val.replace("\"", "\"\"");
    }
}
