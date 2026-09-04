package com.library.erp.specification;

import com.library.erp.entity.Author;
import com.library.erp.entity.Book;
import com.library.erp.entity.BookCopy;
import com.library.erp.entity.enums.BookStatus;
import com.library.erp.entity.enums.CopyStatus;
import jakarta.persistence.criteria.*;
import org.springframework.data.jpa.domain.Specification;

import java.util.ArrayList;
import java.util.List;

public class BookSpecification {

    public static Specification<Book> filter(String keyword,
                                            Long categoryId,
                                            Long authorId,
                                            Long publisherId,
                                            String language,
                                            BookStatus status,
                                            Boolean availableOnly) {
        return (root, query, criteriaBuilder) -> {
            List<Predicate> predicates = new ArrayList<>();

            if (keyword != null && !keyword.trim().isEmpty()) {
                String searchPattern = "%" + keyword.trim().toLowerCase() + "%";
                Predicate titleMatch = criteriaBuilder.like(criteriaBuilder.lower(root.get("title")), searchPattern);
                Predicate isbnMatch = criteriaBuilder.like(criteriaBuilder.lower(root.get("isbn")), searchPattern);
                Predicate subtitleMatch = criteriaBuilder.like(criteriaBuilder.lower(root.get("subtitle")), searchPattern);
                predicates.add(criteriaBuilder.or(titleMatch, isbnMatch, subtitleMatch));
            }

            if (categoryId != null) {
                predicates.add(criteriaBuilder.equal(root.get("category").get("id"), categoryId));
            }

            if (authorId != null) {
                Join<Book, Author> authorJoin = root.join("authors");
                predicates.add(criteriaBuilder.equal(authorJoin.get("id"), authorId));
            }

            if (publisherId != null) {
                predicates.add(criteriaBuilder.equal(root.get("publisher").get("id"), publisherId));
            }

            if (language != null && !language.trim().isEmpty()) {
                predicates.add(criteriaBuilder.equal(criteriaBuilder.lower(root.get("language")), language.trim().toLowerCase()));
            }

            if (status != null) {
                predicates.add(criteriaBuilder.equal(root.get("status"), status));
            }

            if (Boolean.TRUE.equals(availableOnly)) {
                query.distinct(true);
                Join<Book, BookCopy> copyJoin = root.join("copies", JoinType.INNER);
                predicates.add(criteriaBuilder.equal(copyJoin.get("availabilityStatus"), CopyStatus.AVAILABLE));
            }

            return criteriaBuilder.and(predicates.toArray(new Predicate[0]));
        };
    }
}
