# Modernization intent: contoso

Date: 2026-10-26

- **Goal:** reimagine (rebuild from scratch on a new architecture)
- **From:** ASP.NET MVC 5 on .NET Framework 4.8 (ContosoUniversity, `legacy/contoso`)
- **To / vision:** Modular monolith on .NET 8 (ASP.NET Core)
- **What must stay true:** Behavior must match exactly, including known quirks.

## Their answers, word for word
- What do you want to do with it? "Rebuild from scratch"
- What must stay true? "Behavior matches exactly"
- What should it become? "Modular monolith (.NET 8)"
- Code location: "Yes, use this folder" (legacy/contoso is a junction to ContosoUniversity)
