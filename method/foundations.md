# SAM Foundations

SAM synthesizes established architecture practices into a lightweight, agent-assisted workflow. It does not reproduce any source and does not treat a book or method as a substitute for project evidence or architect judgment.

## Source-To-Practice Mapping

| Source | Practices reflected in SAM |
| --- | --- |
| *Fundamentals of Software Architecture, 2nd Edition*, Mark Richards and Neal Ford | Architecture characteristics, tradeoff analysis, breadth of architect responsibility, and evolutionary thinking. |
| *Software Architecture in Practice, 4th Edition*, Len Bass, Paul Clements, and Rick Kazman | Quality attribute scenarios, tactics, business goals, architectural evaluation, and evidence-oriented reasoning. |
| *Documenting Software Architectures: Views and Beyond, 2nd Edition*, Paul Clements et al. | Stakeholder-driven view selection, interfaces and behavior, cross-view information, rationale, and documentation as part of design. |
| *Designing Software Architectures: A Practical Approach, 2nd Edition*, Humberto Cervantes and Rick Kazman | Attribute-Driven Design, reusable design concepts, iteration planning, instantiation, and contemporary cloud/API/deployability concerns. |
| *Patterns of Enterprise Application Architecture*, Martin Fowler | Enterprise application and data patterns used as candidates, never as defaults. |
| *Software Architecture Patterns, 2nd Edition*, Mark Richards | Architectural styles, characteristics, strengths, weaknesses, and contextual selection. |
| *Architectural Patterns*, Anupama Murali, Pethuru Raj, Harihara Subramanian J, and Pethuru Raj Chelliah | Broader pattern vocabulary for candidate concepts and tradeoff discussion. |
| SEI Attribute-Driven Design (ADD) | Iterative selection of an element and relevant ASRs, choice of concepts and tactics, instantiation, interfaces, analysis, and refinement. |
| SEI Quality Attribute Workshop (QAW) | Stakeholder-derived, prioritized, and refined quality attribute scenarios before architecture selection. |
| C4, ADRs, and evolutionary architecture practices | Accessible views where useful, durable decision rationale, review triggers, fitness checks, and architecture-code drift control. |

## How SAM Uses The Foundations

1. Start with business goals, significant functionality, quality scenarios, constraints, assumptions, and concerns.
2. Prioritize the small set that should drive architecture.
3. Apply ADD iteratively to selected elements and ASRs; compare bounded concepts and expose tradeoffs.
4. Record material decisions, consequences, review triggers, and checks as design occurs.
5. Select documentation views from stakeholder questions and intended use, not from a mandatory diagram list.
6. Preserve approved artifacts, source hashes, traceability, and evidence status as living project memory.
7. Convert approved architecture into delivery slices only when the project needs that handoff.

## Interpretation Boundaries

- Patterns and technologies are candidates to evaluate, not answers to infer from project type.
- A quality scenario is useful only when its response or measurement gap is explicit.
- A decision is architecturally significant when it affects structure, qualities, integration, deployment, data ownership, or cost of change.
- Documentation depth follows risk and stakeholder need. Small projects should not imitate the artifact volume of high-assurance systems.
- Agent output remains a proposal until the designated human authority approves it.

## Primary Public References

- [SEI Attribute-Driven Design Method Collection](https://www.sei.cmu.edu/library/attribute-driven-design-method-collection/)
- [SEI Quality Attribute Workshops, Third Edition](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/)
- [SEI Views and Beyond Collection](https://www.sei.cmu.edu/library/views-and-beyond-collection/)
- [Designing Software Architectures: A Practical Approach, 2nd Edition](https://www.sei.cmu.edu/library/designing-software-architectures-a-practical-approach/)
