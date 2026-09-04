"""Multi-Dimensional Faceted Search and Bucket Aggregator."""

from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class FacetBucket:
    value: str
    count: int


@dataclass
class FacetResult:
    facet_name: str
    buckets: List[FacetBucket] = field(default_factory=list)


class FacetEngine:
    """Aggregates catalog search result attributes into categorized facet counts."""

    @staticmethod
    def aggregate_facets(items: List[Dict[str, Any]], facet_fields: List[str]) -> Dict[str, FacetResult]:
        results: Dict[str, FacetResult] = {}
        for f in facet_fields:
            results[f] = FacetResult(facet_name=f)

        for item in items:
            for f in facet_fields:
                val = item.get(f)
                if val:
                    val_str = str(val)
                    # Find or create bucket
                    bucket = None
                    for b in results[f].buckets:
                        if b.value == val_str:
                            bucket = b
                            break
                    if bucket:
                        bucket.count += 1
                    else:
                        results[f].buckets.append(FacetBucket(value=val_str, count=1))

        # Sort buckets descending by count
        for f in facet_fields:
            results[f].buckets.sort(key=lambda b: b.count, reverse=True)

        return results
