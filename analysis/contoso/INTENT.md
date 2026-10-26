# Modernization intent: contoso

Date: 2026-10-26

- **Goal:** reimagine (rebuild from scratch on a new architecture)
- **From:** ASP.NET MVC 5 on .NET Framework 4.8 (ContosoUniversity, `legacy/contoso`)
- **To / vision:** see the Update section below (was: modular monolith on .NET 8)
- **What must stay true:** Behavior must match exactly, including known quirks.

## Their answers, word for word
- What do you want to do with it? "Rebuild from scratch"
- What must stay true? "Behavior matches exactly"
- What should it become? "Modular monolith (.NET 8)"
- Code location: "Yes, use this folder" (legacy/contoso is a junction to ContosoUniversity)

## Update (2026-10-26): refined target, in their words
"The plan should be to rebuild as a modular monolith: one asp.net core (.net 10) rest api container and one react 19 SPA container. Code should be clean architecture projects with vertical slices grouped by bounded contexts."

- **To / vision (supersedes ".NET 8" above):** Modular monolith. Two containers:
  1. One ASP.NET Core (.NET 10) REST API container.
  2. One React 19 SPA container.
- **Code structure:** Clean Architecture projects, with vertical slices grouped by bounded contexts.
- **Still true:** Behavior must match exactly, including known quirks.
