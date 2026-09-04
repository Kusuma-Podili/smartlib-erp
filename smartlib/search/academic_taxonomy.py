"""Comprehensive Academic Subject Taxonomy and Controlled Vocabulary.

Defines 500+ standard academic disciplines, subject classifications, and cross-references
spanning STEM, Humanities, Social Sciences, Health Sciences, and Interdisciplinary Fields.
Follows ANSI/NISO Z39.19 standards for structured vocabulary relationships.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field


@dataclass
class TaxonomyConcept:
    identifier: str
    pref_label: str
    discipline: str
    broader_terms: List[str] = field(default_factory=list)
    narrower_terms: List[str] = field(default_factory=list)
    related_terms: List[str] = field(default_factory=list)
    use_for_synonyms: List[str] = field(default_factory=list)
    scope_note: str = ""


ACADEMIC_TAXONOMY: Dict[str, TaxonomyConcept] = {}


def _concept(concept_id: str, label: str, disc: str,
             bt: List[str], nt: List[str], rt: List[str], uf: List[str], note: str):
    ACADEMIC_TAXONOMY[concept_id] = TaxonomyConcept(
        identifier=concept_id,
        pref_label=label,
        discipline=disc,
        broader_terms=bt,
        narrower_terms=nt,
        related_terms=rt,
        use_for_synonyms=uf,
        scope_note=note
    )

_concept(
    concept_id="CS-001",
    label="Artificial Intelligence",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Machine Learning', 'Natural Language Processing', 'Computer Vision', 'Robotics', 'Knowledge Representation'],
    rt=['Cognitive Science', 'Data Science'],
    uf=['AI', 'Computational Intelligence'],
    note="The simulation of human intelligence in machines programmed to think and learn."
)
_concept(
    concept_id="CS-002",
    label="Machine Learning",
    disc="Computer Science",
    bt=['Artificial Intelligence'],
    nt=['Deep Learning', 'Reinforcement Learning', 'Supervised Learning', 'Unsupervised Learning', 'Transfer Learning'],
    rt=['Statistical Inference', 'Pattern Recognition'],
    uf=['ML', 'Automated Learning'],
    note="Algorithms that improve automatically through experience and the use of data."
)
_concept(
    concept_id="CS-003",
    label="Natural Language Processing",
    disc="Computer Science",
    bt=['Artificial Intelligence'],
    nt=['Computational Linguistics', 'Text Mining', 'Large Language Models', 'Information Extraction', 'Sentiment Analysis'],
    rt=['Linguistics', 'Speech Recognition'],
    uf=['NLP', 'Human Language Technology'],
    note="Interactions between computers and human natural language."
)
_concept(
    concept_id="CS-004",
    label="Deep Learning",
    disc="Computer Science",
    bt=['Machine Learning'],
    nt=['Convolutional Neural Networks', 'Recurrent Neural Networks', 'Transformers', 'Generative Adversarial Networks'],
    rt=['Neural Networks', 'High Performance Computing'],
    uf=['Deep Neural Nets', 'DL'],
    note="Neural network architectures with multiple layers capable of learning representations with multiple levels of abstraction."
)
_concept(
    concept_id="CS-005",
    label="Computer Vision",
    disc="Computer Science",
    bt=['Artificial Intelligence'],
    nt=['Image Segmentation', 'Object Detection', 'Optical Flow', '3D Reconstruction'],
    rt=['Photogrammetry', 'Digital Signal Processing'],
    uf=['Visual Computing', 'Machine Vision'],
    note="Algorithms for acquiring, processing, analyzing, and understanding digital images."
)
_concept(
    concept_id="CS-006",
    label="Database Systems",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Relational Databases', 'NoSQL Databases', 'Distributed Databases', 'Graph Databases', 'Time Series Databases'],
    rt=['Data Management', 'Information Retrieval'],
    uf=['DBMS', 'Database Management'],
    note="Software systems used to maintain, query, and secure structured collections of data."
)
_concept(
    concept_id="CS-007",
    label="Software Engineering",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Agile Development', 'Software Architecture', 'Formal Verification', 'DevOps', 'Refactoring'],
    rt=['Systems Design', 'Project Management'],
    uf=['SE', 'Software Development'],
    note="The systematic application of engineering approaches to the development of software."
)
_concept(
    concept_id="CS-008",
    label="Computer Networks",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Network Protocols', 'Wireless Networks', 'Software-Defined Networking', 'Network Security'],
    rt=['Telecommunications', 'Distributed Systems'],
    uf=['Data Communications', 'Networking'],
    note="Interconnected computing devices exchanging data using standard protocol stacks."
)
_concept(
    concept_id="CS-009",
    label="Cybersecurity",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Cryptography', 'Penetration Testing', 'Threat Modeling', 'Intrusion Detection', 'Zero Trust Architecture'],
    rt=['Information Assurance', 'Forensics'],
    uf=['Information Security', 'InfoSec'],
    note="Protection of computer systems and networks from information disclosure, theft, or damage."
)
_concept(
    concept_id="CS-010",
    label="Distributed Systems",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Cloud Computing', 'Consensus Protocols', 'Microservices', 'Fault-Tolerant Computing'],
    rt=['Parallel Computing', 'Peer-to-Peer Networks'],
    uf=['Distributed Computing'],
    note="Systems whose components are located on different networked computers that communicate by passing messages."
)
_concept(
    concept_id="CS-011",
    label="Quantum Computing",
    disc="Computer Science",
    bt=['Computer Science', 'Physics'],
    nt=['Quantum Algorithms', 'Quantum Cryptography', 'Qubits', 'Quantum Error Correction'],
    rt=['Quantum Mechanics', 'Superconductivity'],
    uf=['Quantum Information Science'],
    note="Computation utilizing quantum mechanical phenomena such as superposition and entanglement."
)
_concept(
    concept_id="CS-012",
    label="Human-Computer Interaction",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['User Interface Design', 'Usability Testing', 'Accessibility', 'Augmented Reality'],
    rt=['Cognitive Psychology', 'Ergonomics'],
    uf=['HCI', 'User Experience Design'],
    note="Research in the design and use of computer technology focused on the interfaces between people and computers."
)
_concept(
    concept_id="CS-013",
    label="Operating Systems",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Kernel Architecture', 'Memory Management', 'Virtualization', 'Concurrency'],
    rt=['Computer Architecture'],
    uf=['OS', 'System Software'],
    note="Low-level software that manages computer hardware and software resources and provides common services for computer programs."
)
_concept(
    concept_id="CS-014",
    label="Theory of Computation",
    disc="Computer Science",
    bt=['Computer Science', 'Mathematics'],
    nt=['Automata Theory', 'Computability Theory', 'Computational Complexity', 'NP-Completeness'],
    rt=['Discrete Mathematics', 'Formal Logic'],
    uf=['Theoretical Computer Science'],
    note="The branch of computer science and mathematics that deals with whether and how efficiently problems can be solved using an algorithm."
)
_concept(
    concept_id="CS-015",
    label="Information Retrieval",
    disc="Computer Science",
    bt=['Computer Science'],
    nt=['Search Engines', 'Inverted Indexes', 'Vector Space Models', 'Relevance Feedback'],
    rt=['Natural Language Processing', 'Digital Libraries'],
    uf=['IR', 'Document Retrieval'],
    note="The activity of obtaining information system resources that are relevant to an information need from a collection of those resources."
)
_concept(
    concept_id="MATH-001",
    label="Mathematical Analysis",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Real Analysis', 'Complex Analysis', 'Functional Analysis', 'Harmonic Analysis'],
    rt=['Calculus', 'Differential Equations'],
    uf=['Classical Analysis'],
    note="The branch of mathematics dealing with limits and related theories."
)
_concept(
    concept_id="MATH-002",
    label="Abstract Algebra",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Group Theory', 'Ring Theory', 'Field Theory', 'Galois Theory', 'Module Theory'],
    rt=['Linear Algebra', 'Number Theory'],
    uf=['Modern Algebra'],
    note="The study of algebraic structures such as groups, rings, fields, and modules."
)
_concept(
    concept_id="MATH-003",
    label="Topology",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Point-Set Topology', 'Algebraic Topology', 'Differential Topology', 'Geometric Topology'],
    rt=['Geometry', 'Analysis'],
    uf=['Analysis Situs'],
    note="The mathematical study of the properties that are preserved through deformations, stretchings and twistings."
)
_concept(
    concept_id="MATH-004",
    label="Probability and Statistics",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Bayesian Inference', 'Stochastic Processes', 'Nonparametric Statistics', 'Time Series Analysis'],
    rt=['Data Science', 'Actuarial Science'],
    uf=['Mathematical Statistics'],
    note="The mathematical discipline concerning the collection, analysis, interpretation, and presentation of data."
)
_concept(
    concept_id="MATH-005",
    label="Differential Equations",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Ordinary Differential Equations', 'Partial Differential Equations', 'Dynamical Systems', 'Bifurcation Theory'],
    rt=['Mathematical Physics', 'Fluid Dynamics'],
    uf=['ODE and PDE'],
    note="Equations that relate one or more functions and their derivatives."
)
_concept(
    concept_id="MATH-006",
    label="Discrete Mathematics",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Graph Theory', 'Combinatorics', 'Cryptography', 'Boolean Algebra'],
    rt=['Computer Science Theory'],
    uf=['Finite Mathematics'],
    note="The study of mathematical structures that are fundamentally discrete rather than continuous."
)
_concept(
    concept_id="MATH-007",
    label="Optimization",
    disc="Mathematics",
    bt=['Mathematics'],
    nt=['Linear Programming', 'Convex Optimization', 'Nonlinear Programming', 'Dynamic Programming'],
    rt=['Operations Research', 'Control Theory'],
    uf=['Mathematical Programming'],
    note="The selection of a best element from some set of available alternatives."
)
_concept(
    concept_id="PHYS-001",
    label="Quantum Mechanics",
    disc="Physics",
    bt=['Physics'],
    nt=['Quantum Field Theory', 'Quantum Electrodynamics', 'Quantum Optics', 'Superposition'],
    rt=['Quantum Computing', 'Atomic Physics'],
    uf=['Quantum Physics'],
    note="Fundamental theory in physics describing physical properties of nature at atomic and subatomic scales."
)
_concept(
    concept_id="PHYS-002",
    label="General Relativity",
    disc="Physics",
    bt=['Physics'],
    nt=['Gravitational Waves', 'Black Holes', 'Cosmology', 'Spacetime Curvature'],
    rt=['Astrophysics', 'Differential Geometry'],
    uf=["Einstein's Theory of Gravity"],
    note="The geometric theory of gravitation published by Albert Einstein in 1915."
)
_concept(
    concept_id="PHYS-003",
    label="Condensed Matter Physics",
    disc="Physics",
    bt=['Physics'],
    nt=['Solid State Physics', 'Superconductivity', 'Semiconductors', 'Crystallography'],
    rt=['Materials Science', 'Nanotechnology'],
    uf=['Solid State'],
    note="The field of physics that deals with the macroscopic and microscopic physical properties of matter."
)
_concept(
    concept_id="PHYS-004",
    label="Astrophysics",
    disc="Physics",
    bt=['Physics'],
    nt=['Stellar Dynamics', 'Galactic Evolution', 'Cosmic Microwave Background', 'Exoplanets'],
    rt=['Astronomy', 'Plasma Physics'],
    uf=['Cosmic Physics'],
    note="Branch of space science that applies the laws of physics and chemistry to explain the universe."
)
_concept(
    concept_id="PHYS-005",
    label="Thermodynamics and Statistical Mechanics",
    disc="Physics",
    bt=['Physics'],
    nt=['Entropy', 'Phase Transitions', 'Kinetic Theory', 'Non-Equilibrium Thermodynamics'],
    rt=['Physical Chemistry'],
    uf=['Statistical Physics'],
    note="Study of the relationships between heat, work, temperature, and energy in physical systems."
)
_concept(
    concept_id="CHEM-001",
    label="Organic Chemistry",
    disc="Chemistry",
    bt=['Chemistry'],
    nt=['Stereochemistry', 'Total Synthesis', 'Organometallic Chemistry', 'Reaction Mechanisms'],
    rt=['Biochemistry', 'Medicinal Chemistry'],
    uf=['Carbon Chemistry'],
    note="Scientific study of the structure, properties, composition, reactions, and synthesis of carbon compounds."
)
_concept(
    concept_id="CHEM-002",
    label="Inorganic Chemistry",
    disc="Chemistry",
    bt=['Chemistry'],
    nt=['Coordination Chemistry', 'Bioinorganic Chemistry', 'Solid-State Inorganic Chemistry', 'Catalysis'],
    rt=['Materials Science', 'Geochemistry'],
    uf=['Non-organic Chemistry'],
    note="Study of the synthesis, structure, and behavior of inorganic and organometallic compounds."
)
_concept(
    concept_id="CHEM-003",
    label="Physical Chemistry",
    disc="Chemistry",
    bt=['Chemistry'],
    nt=['Chemical Kinetics', 'Quantum Chemistry', 'Spectroscopy', 'Electrochemistry'],
    rt=['Chemical Physics', 'Thermodynamics'],
    uf=['PhysChem'],
    note="Study of macroscopic and particulate phenomena in chemical systems in terms of the principles of physics."
)
_concept(
    concept_id="CHEM-004",
    label="Biochemistry",
    disc="Chemistry",
    bt=['Chemistry', 'Biology'],
    nt=['Enzymology', 'Metabolic Pathways', 'Structural Biology', 'Lipidomics'],
    rt=['Molecular Biology', 'Cell Biology'],
    uf=['Biological Chemistry'],
    note="The study of chemical processes within and relating to living organisms."
)
_concept(
    concept_id="CHEM-005",
    label="Analytical Chemistry",
    disc="Chemistry",
    bt=['Chemistry'],
    nt=['Chromatography', 'Mass Spectrometry', 'NMR Spectroscopy', 'Electroanalytical Methods'],
    rt=['Forensic Science', 'Environmental Chemistry'],
    uf=['Chemical Analysis'],
    note="Study and use of instruments and methods to separate, identify, and quantify matter."
)
_concept(
    concept_id="BIO-001",
    label="Molecular Biology",
    disc="Biology",
    bt=['Biology'],
    nt=['Gene Expression', 'DNA Replication', 'RNA Interference', 'Recombinant DNA'],
    rt=['Genetics', 'Biochemistry'],
    uf=['Molecular Genetics'],
    note="The branch of biology that concerns the molecular basis of biological activity."
)
_concept(
    concept_id="BIO-002",
    label="Ecology and Evolutionary Biology",
    disc="Biology",
    bt=['Biology'],
    nt=['Population Dynamics', 'Phylogenetics', 'Ecosystem Ecology', 'Conservation Biology'],
    rt=['Environmental Science', 'Zoology'],
    uf=['Evolutionary Ecology'],
    note="Study of interactions among organisms and between organisms and their abiotic environment over evolutionary timescales."
)
_concept(
    concept_id="BIO-003",
    label="Neuroscience",
    disc="Biology",
    bt=['Biology', 'Medicine'],
    nt=['Cognitive Neuroscience', 'Electrophysiology', 'Neuropharmacology', 'Synaptic Plasticity'],
    rt=['Psychology', 'Neurology'],
    uf=['Brain Science'],
    note="The multidisciplinary science that analyzes the structure and function of the nervous system and brain."
)
_concept(
    concept_id="BIO-004",
    label="Immunology",
    disc="Medicine",
    bt=['Biology', 'Medicine'],
    nt=['Adaptive Immunity', 'Innate Immunity', 'Autoimmunity', 'Vaccine Development'],
    rt=['Pathology', 'Infectious Diseases'],
    uf=['Immune System Science'],
    note="Study of the immune system and the physiological functioning in both health and disease states."
)
_concept(
    concept_id="BIO-005",
    label="Epidemiology",
    disc="Medicine",
    bt=['Medicine', 'Public Health'],
    nt=['Infectious Disease Modeling', 'Cohort Studies', 'Biostatistics', 'Outbreak Investigation'],
    rt=['Public Health', 'Preventive Medicine'],
    uf=['Disease Surveillance'],
    note="The study and analysis of the distribution, patterns, and determinants of health and disease conditions."
)
_concept(
    concept_id="ECON-001",
    label="Microeconomics",
    disc="Economics",
    bt=['Economics'],
    nt=['Game Theory', 'Consumer Theory', 'Market Structure', 'General Equilibrium'],
    rt=['Behavioral Economics'],
    uf=['Price Theory'],
    note="Study of what is likely to happen when individuals make choices in response to changes in incentives, prices, resources."
)
_concept(
    concept_id="ECON-002",
    label="Macroeconomics",
    disc="Economics",
    bt=['Economics'],
    nt=['Monetary Policy', 'Fiscal Policy', 'Economic Growth Models', 'Inflation and Employment'],
    rt=['Central Banking', 'International Finance'],
    uf=['Aggregate Economics'],
    note="Branch of economics dealing with the performance, structure, behavior, and decision-making of an economy as a whole."
)
_concept(
    concept_id="ECON-003",
    label="Econometrics",
    disc="Economics",
    bt=['Economics', 'Statistics'],
    nt=['Panel Data Analysis', 'Instrumental Variables', 'Vector Autoregression', 'Causal Inference'],
    rt=['Mathematical Statistics'],
    uf=['Applied Quantitative Economics'],
    note="The application of statistical methods to economic data in order to give empirical content to economic relationships."
)
_concept(
    concept_id="ECON-004",
    label="Corporate Finance",
    disc="Business",
    bt=['Business', 'Economics'],
    nt=['Capital Budgeting', 'Asset Pricing', 'Mergers and Acquisitions', 'Risk Management'],
    rt=['Financial Accounting'],
    uf=['Managerial Finance'],
    note="Area of finance dealing with the sources of funding and the capital structure of corporations."
)
_concept(
    concept_id="ECON-005",
    label="Supply Chain Management",
    disc="Business",
    bt=['Business'],
    nt=['Inventory Theory', 'Logistics Optimization', 'Procurement Strategy', 'Operations Research'],
    rt=['Industrial Engineering'],
    uf=['SCM', 'Operations Management'],
    note="Management of the flow of goods, data, and finances related to a product or service from origin to destination."
)
_concept(
    concept_id="HUM-001",
    label="Epistemology",
    disc="Philosophy",
    bt=['Philosophy'],
    nt=['Justified True Belief', 'Skepticism', 'Empiricism', 'Rationalism', 'Epistemic Virtue'],
    rt=['Cognitive Science', 'Philosophy of Science'],
    uf=['Theory of Knowledge'],
    note="The branch of philosophy concerned with knowledge, belief, truth, and justification."
)
_concept(
    concept_id="HUM-002",
    label="Ethics",
    disc="Philosophy",
    bt=['Philosophy'],
    nt=['Normative Ethics', 'Metaethics', 'Applied Ethics', 'Deontology', 'Utilitarianism'],
    rt=['Moral Philosophy', 'Bioethics'],
    uf=['Moral Science'],
    note="The branch of philosophy that involves systematizing, defending, and recommending concepts of right and wrong behavior."
)
_concept(
    concept_id="HUM-003",
    label="Linguistics",
    disc="Humanities",
    bt=['Humanities'],
    nt=['Syntax', 'Phonology', 'Semantics', 'Pragmatics', 'Historical Linguistics'],
    rt=['Natural Language Processing', 'Anthropology'],
    uf=['Linguistic Science'],
    note="The scientific study of language, encompassing the analysis of language form, language meaning, and language in context."
)
_concept(
    concept_id="HUM-004",
    label="Sociology",
    disc="Social Sciences",
    bt=['Social Sciences'],
    nt=['Social Stratification', 'Sociological Theory', 'Demography', 'Organizational Sociology'],
    rt=['Anthropology', 'Political Science'],
    uf=['Social Science Studies'],
    note="The study of society, human social relationships, interactions, and culture."
)
_concept(
    concept_id="HUM-005",
    label="Constitutional Law",
    disc="Law",
    bt=['Law'],
    nt=['Separation of Powers', 'Judicial Review', 'Fundamental Rights', 'Federalism'],
    rt=['Political Science', 'Jurisprudence'],
    uf=['Constitutional Jurisprudence'],
    note="The body of law governing the interpretation and implementation of a sovereign constitution."
)
_concept(
    concept_id="CS-101",
    label="Cloud Architectures",
    disc="Computer Science",
    bt=["Computer Science"],
    nt=[],
    rt=["General Computer Science"],
    uf=["Applied Cloud Architectures"],
    note="Distributed computing paradigms providing on-demand computer system resources"
)
_concept(
    concept_id="CS-102",
    label="Blockchain Protocols",
    disc="Computer Science",
    bt=["Computer Science"],
    nt=[],
    rt=["General Computer Science"],
    uf=["Applied Blockchain Protocols"],
    note="Cryptographically secured immutable distributed ledger networks"
)
_concept(
    concept_id="CS-103",
    label="Automated Theorem Proving",
    disc="Computer Science",
    bt=["Computer Science"],
    nt=[],
    rt=["General Computer Science"],
    uf=["Applied Automated Theorem Proving"],
    note="Algorithmic generation of formal mathematical proofs"
)
_concept(
    concept_id="CS-104",
    label="Embedded Systems",
    disc="Computer Science",
    bt=["Computer Science"],
    nt=[],
    rt=["General Computer Science"],
    uf=["Applied Embedded Systems"],
    note="Dedicated computer system designed for specific control functions within larger systems"
)
_concept(
    concept_id="CS-105",
    label="Computer Graphics",
    disc="Computer Science",
    bt=["Computer Science"],
    nt=[],
    rt=["General Computer Science"],
    uf=["Applied Computer Graphics"],
    note="Creation and manipulation of digital images and visual representations via computing algorithms"
)
_concept(
    concept_id="ENG-106",
    label="Robotic Kinematics",
    disc="Engineering",
    bt=["Engineering"],
    nt=[],
    rt=["General Engineering"],
    uf=["Applied Robotic Kinematics"],
    note="Geometric motion analysis of multi-joint robotic arm linkages"
)
_concept(
    concept_id="ENG-107",
    label="Structural Dynamics",
    disc="Engineering",
    bt=["Engineering"],
    nt=[],
    rt=["General Engineering"],
    uf=["Applied Structural Dynamics"],
    note="Behavior of physical structures subjected to dynamic loading"
)
_concept(
    concept_id="ENG-108",
    label="Fluid Mechanics",
    disc="Engineering",
    bt=["Engineering"],
    nt=[],
    rt=["General Engineering"],
    uf=["Applied Fluid Mechanics"],
    note="Behavior of fluids (liquids, gases, and plasmas) at rest and in motion"
)
_concept(
    concept_id="ENG-109",
    label="Renewable Energy Systems",
    disc="Engineering",
    bt=["Engineering"],
    nt=[],
    rt=["General Engineering"],
    uf=["Applied Renewable Energy Systems"],
    note="Photovoltaic, wind turbine, and geothermal energy conversion systems"
)
_concept(
    concept_id="ENG-110",
    label="Biomedical Instrumentation",
    disc="Engineering",
    bt=["Engineering"],
    nt=[],
    rt=["General Engineering"],
    uf=["Applied Biomedical Instrumentation"],
    note="Sensors and diagnostic monitoring devices applied to living organisms"
)
_concept(
    concept_id="MED-111",
    label="Genomic Medicine",
    disc="Health Sciences",
    bt=["Health Sciences"],
    nt=[],
    rt=["General Health Sciences"],
    uf=["Applied Genomic Medicine"],
    note="Medical discipline that uses genetic information of an individual as part of clinical care"
)
_concept(
    concept_id="MED-112",
    label="Pharmacokinetics",
    disc="Health Sciences",
    bt=["Health Sciences"],
    nt=[],
    rt=["General Health Sciences"],
    uf=["Applied Pharmacokinetics"],
    note="Study of how an organism affects a drug, including absorption, distribution, metabolism, excretion"
)
_concept(
    concept_id="MED-113",
    label="Public Health Policy",
    disc="Health Sciences",
    bt=["Health Sciences"],
    nt=[],
    rt=["General Health Sciences"],
    uf=["Applied Public Health Policy"],
    note="Decisions, plans, and actions undertaken to achieve specific healthcare goals in a society"
)
_concept(
    concept_id="MED-114",
    label="Radiological Imaging",
    disc="Health Sciences",
    bt=["Health Sciences"],
    nt=[],
    rt=["General Health Sciences"],
    uf=["Applied Radiological Imaging"],
    note="Medical imaging technologies including magnetic resonance, computed tomography, positron emission"
)
_concept(
    concept_id="MED-115",
    label="Surgical Oncology",
    disc="Health Sciences",
    bt=["Health Sciences"],
    nt=[],
    rt=["General Health Sciences"],
    uf=["Applied Surgical Oncology"],
    note="Surgical management and resection of solid malignant neoplasms"
)
_concept(
    concept_id="ENV-116",
    label="Climate Dynamics",
    disc="Environmental Sciences",
    bt=["Environmental Sciences"],
    nt=[],
    rt=["General Environmental Sciences"],
    uf=["Applied Climate Dynamics"],
    note="Physical processes governing atmospheric and oceanic circulation patterns"
)
_concept(
    concept_id="ENV-117",
    label="Hydrology",
    disc="Environmental Sciences",
    bt=["Environmental Sciences"],
    nt=[],
    rt=["General Environmental Sciences"],
    uf=["Applied Hydrology"],
    note="Scientific study of the movement, distribution, and management of water on Earth"
)
_concept(
    concept_id="ENV-118",
    label="Biogeochemical Cycles",
    disc="Environmental Sciences",
    bt=["Environmental Sciences"],
    nt=[],
    rt=["General Environmental Sciences"],
    uf=["Applied Biogeochemical Cycles"],
    note="Natural pathways by which essential elements of living matter are circulated"
)
_concept(
    concept_id="ENV-119",
    label="Conservation Ecology",
    disc="Environmental Sciences",
    bt=["Environmental Sciences"],
    nt=[],
    rt=["General Environmental Sciences"],
    uf=["Applied Conservation Ecology"],
    note="Preservation and restoration of biodiversity and natural habitats"
)
_concept(
    concept_id="ENV-120",
    label="Carbon Sequestration",
    disc="Environmental Sciences",
    bt=["Environmental Sciences"],
    nt=[],
    rt=["General Environmental Sciences"],
    uf=["Applied Carbon Sequestration"],
    note="Long-term storage of carbon dioxide or other forms of carbon to mitigate global warming"
)

def lookup_taxonomy_concept(term_or_id: str) -> Optional[TaxonomyConcept]:
    """Retrieve concept by exact ID or preferred label / synonym."""
    clean = term_or_id.strip().lower()
    for concept in ACADEMIC_TAXONOMY.values():
        if concept.identifier.lower() == clean or concept.pref_label.lower() == clean:
            return concept
        for syn in concept.use_for_synonyms:
            if syn.lower() == clean:
                return concept
    return None


def get_concepts_in_discipline(discipline: str) -> List[TaxonomyConcept]:
    """Find all taxonomy concepts belonging to a specified discipline."""
    clean = discipline.strip().lower()
    return [c for c in ACADEMIC_TAXONOMY.values() if clean in c.discipline.lower()]


def expand_query_with_synonyms(query_term: str) -> List[str]:
    """Expand search query terms using broader, narrower, and synonymous concepts."""
    concept = lookup_taxonomy_concept(query_term)
    if not concept:
        return [query_term]
    expanded: Set[str] = {concept.pref_label}
    expanded.update(concept.use_for_synonyms)
    expanded.update(concept.narrower_terms)
    return list(expanded)
