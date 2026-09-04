package com.library.erp.controller.librarian;

import com.library.erp.entity.enums.ReservationStatus;
import com.library.erp.repository.ReservationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/librarian/reservations")
@PreAuthorize("hasAnyRole('LIBRARIAN', 'ADMIN')")
@RequiredArgsConstructor
public class LibrarianReservationController {

    private final ReservationRepository reservationRepository;

    @GetMapping
    public String viewQueue(Model model) {
        model.addAttribute("pendingHolds", reservationRepository.countByStatus(ReservationStatus.PENDING));
        model.addAttribute("notifiedHolds", reservationRepository.countByStatus(ReservationStatus.NOTIFIED));
        model.addAttribute("reservations", reservationRepository.findAll(
                PageRequest.of(0, 30, Sort.by("reservationDate").descending())
        ).getContent());
        model.addAttribute("activeMenu", "lib-reservations");
        return "librarian/circulation/reservations";
    }
}
