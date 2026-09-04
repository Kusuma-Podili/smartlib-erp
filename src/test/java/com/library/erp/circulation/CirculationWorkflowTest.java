package com.library.erp.circulation;

import com.library.erp.dto.catalog.AuthorDto;
import com.library.erp.dto.catalog.BookRequestDto;
import com.library.erp.dto.catalog.CategoryDto;
import com.library.erp.dto.catalog.PublisherDto;
import com.library.erp.dto.circulation.BorrowRequestDto;
import com.library.erp.dto.circulation.FinePaymentDto;
import com.library.erp.dto.circulation.ReturnProcessDto;
import com.library.erp.dto.member.MemberRegistrationDto;
import com.library.erp.dto.member.MembershipTypeDto;
import com.library.erp.entity.*;
import com.library.erp.entity.enums.*;
import com.library.erp.exception.BusinessRuleViolationException;
import com.library.erp.repository.BorrowRecordRepository;
import com.library.erp.service.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Set;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class CirculationWorkflowTest {

    @Autowired
    private BookService bookService;

    @Autowired
    private BookCopyService bookCopyService;

    @Autowired
    private CategoryService categoryService;

    @Autowired
    private AuthorService authorService;

    @Autowired
    private PublisherService publisherService;

    @Autowired
    private MemberService memberService;

    @Autowired
    private MembershipTypeService membershipTypeService;

    @Autowired
    private BorrowService borrowService;

    @Autowired
    private ReturnService returnService;

    @Autowired
    private FineService fineService;

    @Autowired
    private ReservationService reservationService;

    @Autowired
    private BorrowRecordRepository borrowRecordRepository;

    private Member testMember;
    private Book testBook;
    private BookCopy testCopy;

    @BeforeEach
    void setUp() {
        MembershipType tier = membershipTypeService.createMembershipType(MembershipTypeDto.builder()
                .name("StrictTestTier_" + System.currentTimeMillis())
                .borrowingLimit(2) // strict limit of 2
                .borrowDurationDays(14)
                .gracePeriodDays(1)
                .finePerDay(BigDecimal.valueOf(10.00))
                .build());

        String unique = "circ_" + System.currentTimeMillis();
        testMember = memberService.registerMember(MemberRegistrationDto.builder()
                .username(unique)
                .email(unique + "@library.test")
                .firstName("Circulation")
                .lastName("Tester")
                .membershipTypeId(tier.getId())
                .build());

        Category cat = categoryService.createCategory(CategoryDto.builder()
                .name("Fiction " + System.currentTimeMillis())
                .code("FIC_" + System.currentTimeMillis())
                .build());

        Publisher pub = publisherService.createPublisher(PublisherDto.builder()
                .name("O'Reilly " + System.currentTimeMillis())
                .build());

        Author auth = authorService.createAuthor(AuthorDto.builder()
                .firstName("Martin")
                .lastName("Fowler")
                .build());

        String isbn = "978" + (System.currentTimeMillis() % 10000000000L);
        testBook = bookService.createBook(BookRequestDto.builder()
                .isbn(isbn)
                .title("Patterns of Enterprise Application Architecture")
                .categoryId(cat.getId())
                .publisherId(pub.getId())
                .authorIds(Set.of(auth.getId()))
                .initialCopies(1)
                .build());

        testCopy = bookCopyService.findCopiesByBookId(testBook.getId()).get(0);
    }

    @Test
    @DisplayName("Test 1: Checkout assigns copy, sets due date, and changes copy status to BORROWED")
    void borrowBookSuccessWorkflow() {
        BorrowRequestDto req = BorrowRequestDto.builder()
                .memberCode(testMember.getMemberCode())
                .barcode(testCopy.getBarcode())
                .build();

        BorrowRecord record = borrowService.issueBook(req, null);

        assertThat(record.getId()).isNotNull();
        assertThat(record.getStatus()).isEqualTo(BorrowStatus.ISSUED);
        assertThat(record.getDueDate()).isEqualTo(LocalDate.now().plusDays(14));

        BookCopy updatedCopy = bookCopyService.findById(testCopy.getId()).orElseThrow();
        assertThat(updatedCopy.getAvailabilityStatus()).isEqualTo(CopyStatus.BORROWED);
        assertThat(testBook.getAvailableCopiesCount()).isEqualTo(0);
    }

    @Test
    @DisplayName("Test 2: Exceeding membership tier borrowing limit is rejected")
    void borrowingBeyondLimitThrowsException() {
        // First loan
        borrowService.issueBook(BorrowRequestDto.builder()
                .memberCode(testMember.getMemberCode())
                .barcode(testCopy.getBarcode())
                .build(), null);

        // Provision second book copy
        List<BookCopy> moreCopies = bookService.addCopies(testBook.getId(), 2, CopyCondition.NEW);
        BookCopy copy2 = moreCopies.get(0);
        BookCopy copy3 = moreCopies.get(1);

        // Second loan (reaches limit of 2)
        borrowService.issueBook(BorrowRequestDto.builder()
                .memberCode(testMember.getMemberCode())
                .barcode(copy2.getBarcode())
                .build(), null);

        // Third loan must fail
        assertThatThrownBy(() -> borrowService.issueBook(BorrowRequestDto.builder()
                .memberCode(testMember.getMemberCode())
                .barcode(copy3.getBarcode())
                .build(), null))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessageContaining("Borrowing limit reached");
    }

    @Test
    @DisplayName("Test 3: Returning an overdue book computes fine with grace period deduction")
    void returnOverdueBookCalculatesFine() {
        BorrowRecord loan = borrowService.issueBook(BorrowRequestDto.builder()
                .memberCode(testMember.getMemberCode())
                .barcode(testCopy.getBarcode())
                .build(), null);

        // Simulate overdue by backdating due date to 5 days ago
        loan.setDueDate(LocalDate.now().minusDays(5));
        borrowRecordRepository.save(loan);

        // Grace period is 1 day, late days = 5, billable = 4 days @ ₹10/day = ₹40.00
        ReturnRecord returnRecord = returnService.processReturn(ReturnProcessDto.builder()
                .barcode(testCopy.getBarcode())
                .condition(CopyCondition.GOOD)
                .build(), null);

        assertThat(returnRecord.getDaysOverdue()).isEqualTo(5);
        assertThat(returnRecord.getFineAssessed()).isEqualByComparingTo("40.00");

        BookCopy returnedCopy = bookCopyService.findById(testCopy.getId()).orElseThrow();
        assertThat(returnedCopy.getAvailabilityStatus()).isEqualTo(CopyStatus.AVAILABLE);

        BigDecimal balance = fineService.getOutstandingBalanceForMember(testMember.getId());
        assertThat(balance).isEqualByComparingTo("40.00");
    }

    @Test
    @DisplayName("Test 4: Fine payment records cashier receipt and updates outstanding balance")
    void finePaymentGeneratesReceipt() {
        Fine fine = fineService.createFine(null, testMember, FineType.LATE_RETURN, BigDecimal.valueOf(50.00), "Late fee");

        FinePayment payment = fineService.recordPayment(FinePaymentDto.builder()
                .fineId(fine.getId())
                .amountPaid(BigDecimal.valueOf(50.00))
                .paymentMethod(PaymentMethod.CASH)
                .build(), null);

        assertThat(payment.getReceiptNumber()).startsWith("REC-");
        assertThat(payment.getAmountPaid()).isEqualByComparingTo("50.00");

        Fine updatedFine = fineService.findById(fine.getId()).orElseThrow();
        assertThat(updatedFine.getStatus()).isEqualTo(FineStatus.PAID);
    }

    @Test
    @DisplayName("Test 5: Reservation queue prevents duplicate holds and assigns queue positions")
    void reservationQueueOrderAndDuplicateRejection() {
        // Place first hold
        Reservation res1 = reservationService.reserveBook(testMember.getId(), testBook.getId(), "First reservation");
        assertThat(res1.getQueuePosition()).isEqualTo(1);
        assertThat(res1.getStatus()).isEqualTo(ReservationStatus.PENDING);

        // Duplicate hold attempt by same member on same book must fail
        assertThatThrownBy(() -> reservationService.reserveBook(testMember.getId(), testBook.getId(), "Duplicate"))
                .isInstanceOf(BusinessRuleViolationException.class)
                .hasMessageContaining("already have an active hold");
    }
}
