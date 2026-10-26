# Preflight: contoso

Date: 2026-10-26
Source: `legacy/contoso` is a Windows junction to `D:\src\dotnet-migration-copilot-samples\ContosoUniversity`
Target: .NET 10 modular monolith: ASP.NET Core REST API + React 19 SPA, Clean Architecture with vertical slices per bounded context (see `INTENT.md`)

## Answers

1. **Scope:** Is this code the complete system, or one slice of a larger codebase? If a slice, what outside it depends on code inside it, and is breaking those consumers acceptable?
   > Complete system
2. **Build & test locally:** Can this environment restore, build, and run the tests? Roughly how long does the full CI pipeline take?
   > Yes, builds here

   *Open item:* CI duration not given. No CI definition exists in the repo, and the legacy solution has no test project (see Check 3).
3. **Bespoke build infrastructure:** Is there organization-specific build or dependency machinery a newcomer would not guess? Where is it documented?
   > None
4. **Prior attempts:** Has anyone tried to modernize this before? What went wrong?
   > No prior attempts
5. **Off limits:** Is anything in this code not allowed to change in this pass?
   > Nothing off limits

## Scope boundary (Check 6)

Standalone. The repository `dotnet-migration-copilot-samples` holds only this one sample: one `.sln` with one `.csproj`, no project references, no shared includes, and no parent build files. Nothing outside depends on it (no inbound consumers), and it depends on nothing outside except public NuGet packages (no outbound dependencies).

## Checks

| # | Check | Status | Found | Fix |
|---|---|---|---|---|
| 0 | Human answers | ✅ | All 5 answered; CI duration is an open item | — |
| 1 | Stack | ✅ | ASP.NET MVC 5.2.9 on .NET Framework 4.8 (old-style `.csproj` + `packages.config`), EF Core 3.1.32 on SQL Server LocalDB, Razor views, jQuery 3.7 / Bootstrap 5.3, **MSMQ** (`System.Messaging`, `Services/NotificationService.cs`), local-disk uploads (`~/Uploads/TeachingMaterials`). Files: 31 `.cs`, 27 `.cshtml`, 16 `.js`, 3 `.config` | — |
| 2 | Analysis tools | ⚠️ | `python` / `py -3` = Python 3.13.15 ✅. `python3` is the Microsoft Store stub and does **not** run, so use `python` wherever a command says `python3`. `scc`, `cloc` and `lizard` are missing | `winget install benboyter.scc` (or `scoop install scc`); `python -m pip install lizard` (only needed for portfolio assess) |
| 3a | Build definition | ⚠️ | No CI pipeline, `Directory.Build.props`, `nuget.config` or `global.json`. Dependencies come from public nuget.org via `packages.config`. Built with VS 18 Community MSBuild 18.11. Nothing bespoke | — |
| 3b | Legacy build (Level 2) | ⚠️ | On a scratch copy: solution restore succeeded (45 packages, nuget.org). Build **failed**: `MSB3644: The reference assemblies for .NETFramework,Version=v4.8 were not found`. Installed packs: v4.0–v4.7.2 only. A diagnostic build retargeted to v4.7.2 **succeeded**, so the code itself compiles. Restore warns `NU1903`: Microsoft.Data.SqlClient 2.1.4 has a high-severity vulnerability (GHSA-98g6-xh36-x2p7). **No tests exist** | Install the .NET Framework 4.8 Developer Pack (VS Installer → Individual components → ".NET Framework 4.8 targeting pack", or https://aka.ms/msbuild/developerpacks) |
| 3c | Legacy runtime deps | ⚠️ | LocalDB `MSSQLLocalDB` present ✅. The MSMQ Windows feature is **not installed**, so the notification queue (`.\Private$\ContosoUniversityNotifications`) cannot run locally | Only needed for a legacy dual run: `Enable-WindowsOptionalFeature -Online -FeatureName MSMQ-Server` (admin) |
| 3d | Target stack | ✅ | Throwaway projects, built and deleted: .NET SDK 10.0.402 `webapi` + xUnit, 1 test passed; Vite React-TS with **React 19.3.1** + Vitest, 1 test passed; `vite build` OK. Node 24.20.0, npm 12.2.0. Docker 29.9.2, Linux engine (for the two containers) | — |
| 4 | Source completeness | ✅ | No missing includes (Views/Shared/_Layout present; every controller has its views). Data definitions: EF model in `Data/SchoolContext.cs` + seed data in `DbInitializer.cs`. Schema is made by `EnsureCreated()`; there are no migrations or DDL. Config: `Web.config`, `Global.asax`, `App_Start/`. No source-less binaries (the 2 `.map` files are JS source maps) | — |
| 5 | Optional context | ⚠️ | No APM/telemetry. Git history is shallow (6 commits, of which 2 are this setup), so change-frequency risk ranking will be weak | — |
| 6 | Scope boundary | ✅ | Standalone (see above) | — |
| 7 | Source protection | ⚠️ | No `Edit` deny rule in `ContosoUniversity/.claude/settings.json` or the user settings. **Important:** the session currently runs from *inside* the legacy folder, so a project-relative `Edit(/legacy/**)` would not match | See below |

### Check 7 detail

Best fix: start Claude Code from `D:\src\dotnet-migration-copilot-samples`, the folder that holds `analysis/` and `legacy/`. Then add this to `D:\src\dotnet-migration-copilot-samples\.claude\settings.json`. It covers both the junction and its real target:

```json
{ "permissions": { "deny": [
  "Edit(/legacy/**)",
  "Edit(//d/src/dotnet-migration-copilot-samples/ContosoUniversity/**)"
] } }
```

A permission rule covers Claude's file tools and the shell commands it recognizes (`sed`, `tee`, `> file`). It does not cover a script that opens the files itself. The only hard guarantee is at the operating-system level: a read-only copy or folder ACL. Managed (organization) settings were not read.

## Verdict per command

| Command | Verdict | Why |
|---|---|---|
| `assess` | Ready-with-gaps | No `scc`, so LOC/complexity fall back to `find` + `wc` and the COCOMO estimate is coarser |
| `map` | Ready | Python 3.13 via `python` |
| `extract-rules` | Ready | Small, complete source |
| `brief` | Ready | Needs only the discovery artifacts |
| `reimagine` | Ready-with-gaps | Target stack proven (.NET 10, React 19, Docker Linux). Legacy can't build (no 4.8 pack) or run notifications (no MSMQ) and has no tests, so "behavior matches exactly" falls back to recorded traces until those are installed |
| `transform` | Ready-with-gaps | Same as reimagine |
| `harden` | Ready-with-gaps | No SAST tool installed; NuGet audit already flags SqlClient 2.1.4 |
| `uplift` | n/a | Not the chosen road (rebuild) |

**Most important fix:** install the .NET Framework 4.8 Developer Pack. Your goal is exact behavior parity, which needs the legacy app running next to the new one, and the legacy build is blocked only by this pack.

**Next:** `/code-modernization:modernize-assess contoso`
