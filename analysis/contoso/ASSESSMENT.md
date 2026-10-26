# Assessment: contoso

Date: 2026-10-26
Source: `legacy/contoso` (Windows junction to `ContosoUniversity/`)
Tooling: `scc` and `cloc` are not installed, so line counts come from `find` + `wc -l` (non-blank lines; C# also excludes `//` comment lines), and complexity is ranked by counting decision keywords (`if`/`for`/`foreach`/`while`/`case`/`catch`/`&&`/`||`/`??`). Deep analysis was done by three subagents (structure, technical debt, security), and the headline findings were re-checked against the source.

## Executive Summary

Contoso University is a small ASP.NET MVC 5 application on .NET Framework 4.8 (≈4.0 KSLOC first-party: 1.7k C#, 1.4k Razor). It does student, course, instructor and department CRUD, uploads teaching-material images to local disk, and sends real-time admin notifications through MSMQ. The system is small and the code is simple; the most complex file has 33 decision points. The risk is concentrated in a few places. There is **no authentication at all**, so every create, edit and delete is anonymous. An overposting flaw lets **any visitor delete any file under the web root**. The notification feed has a stored-XSS path. The app also depends on three Windows/.NET Framework-only technologies (System.Web, MSMQ, EF Core 3.1 at end of life), and there are **no tests**. Recommendation: **Rebuild** (`/code-modernization:modernize-reimagine contoso`) as the .NET 10 API + React 19 modular monolith already chosen in `INTENT.md`. Before that, pin the current behavior with characterization tests and extracted business rules, because the intent requires an exact behavioral match, quirks included.

## System Inventory

| Item | Value | Evidence |
|---|---|---|
| Runtime | .NET Framework 4.8, ASP.NET MVC 5.2.9, Razor 3.2.9 | `ContosoUniversity.csproj:16`, `packages.config:7-8` |
| Build | Old-style `.csproj` + `packages.config` (45 packages), one `.sln`, one project; ~20 binding redirects | `ContosoUniversity.sln`, `Web.config:44-131` |
| Data | EF Core 3.1.32 → SQL Server LocalDB, `EnsureCreated()` + seed; no migrations, no DDL | `Data/SchoolContext.cs`, `Data/DbInitializer.cs:12`, `Web.config:11` |
| Schema | 7 tables: Person (TPH Student/Instructor), Course, Department (RowVersion concurrency), Enrollment, CourseAssignment, OfficeAssignment, Notification (unused) | `Data/SchoolContext.cs:14-74` |
| Messaging | MSMQ private queue `.\Private$\ContosoUniversityNotifications` (System.Messaging) | `Services/NotificationService.cs`, `Web.config:19` |
| File storage | Local disk `~/Uploads/TeachingMaterials/` under web root | `Controllers/CoursesController.cs:76,159` |
| Front end | Razor views, jQuery, Bootstrap, polling script `notifications.js` (5 s) | `Views/Shared/_Layout.cshtml:39`, `Scripts/notifications.js:28,36` |
| Shipped JS vs manifest | Files on disk are jQuery **3.4.1**, Bootstrap JS **3.4.1**, jquery.validate **1.17.0**; `packages.config` claims 3.7.1 / 5.3.3 / 1.21.0 | `Scripts/jquery-3.4.1.js`, `Scripts/bootstrap.js:1` |
| Auth | None. Global `AuthorizeAttribute` commented out; user hardcoded to `"System"` | `App_Start/FilterConfig.cs:11`, `Controllers/BaseController.cs:28` |
| Tests | **None** (no test project) | `ContosoUniversity.sln` |
| CI | None in repo | — |
| Telemetry | None | — |

**Size (first-party, non-blank)**

| Language | Files | SLOC |
|---|---|---|
| C# | 31 | 1,662 |
| Razor (`.cshtml`) | 27 | 1,357 |
| CSS (`Site.css`, `notifications.css`) | 2 | 625 |
| Config (`Web.config` ×2, `packages.config`) | 3 | 226 |
| JavaScript (`notifications.js`) | 1 | 129 |
| **Total first-party** | **64** | **3,999** |
| Vendor JS (jQuery, Bootstrap, validate, Modernizr, Respond); excluded | 15 | ~12,200 raw |

**Most complex files (decision keywords / lines)**

| File | Decisions | Lines |
|---|---|---|
| `Controllers/CoursesController.cs` | 33 | 263 |
| `Controllers/InstructorsController.cs` | 27 | 261 |
| `Controllers/StudentsController.cs` | 27 | 232 |
| `Controllers/DepartmentsController.cs` | 18 | 176 |
| `Data/DbInitializer.cs` | 10 | 251 |
| `Services/NotificationService.cs` | 8 | 120 |
| `Views/Instructors/Index.cshtml` (Razor) | 9 | 128 |

Total ≈135 decision points in 1.66 KSLOC of C# (≈81 per KSLOC). No god objects; the largest file is 263 lines.

## Architecture at a Glance

Eight domains: five business areas and three cross-cutting ones. Every controller inherits `BaseController`, which creates its own `SchoolContext` and `NotificationService` for each request. There is no DI and no service layer: controllers query EF directly. Diagram: [`ARCHITECTURE.mmd`](ARCHITECTURE.mmd).

| Domain | Key files | Responsibilities | Depends on |
|---|---|---|---|
| D1 Startup and Shell | `Global.asax.cs`, `App_Start/*`, `Web.config`, `Views/Shared/_Layout.cshtml` | `Application_Start`: filters → routes → bundles → `EnsureCreated` + seed; single convention route; layout loads the notification JS on every page | D2, D7 |
| D2 Data Access and Schema | `Data/SchoolContext.cs`, `SchoolContextFactory.cs`, `DbInitializer.cs`, `PaginatedList.cs` | 9 DbSets, TPH Person, composite key on CourseAssignment, all DateTime → `datetime2`, seed data | SQL LocalDB |
| D3 Shared Controller Base | `Controllers/BaseController.cs` | Per-request DbContext + MSMQ handle; `SendEntityNotification` swallows errors | D2, D7 |
| D4 Students | `StudentsController.cs`, `Views/Students/*` | Search, sort, page (10 rows), details with enrollments, CRUD, date validation | D3, D2, D7 |
| D5 Courses and Uploads | `CoursesController.cs`, `Views/Courses/*` | Course CRUD; image upload (extension allow-list, 5 MB, `course_{id}_{guid}.ext`); delete old/orphaned files | D3, D2, D7, local disk |
| D6 Instructors and Departments | `InstructorsController.cs`, `DepartmentsController.cs`, `Views/Instructors/*`, `Views/Departments/*` | Master-detail instructor index; course-assignment checkboxes; office assignment; department CRUD with optimistic concurrency | D3, D2, D7 |
| D7 Notifications (MSMQ) | `Services/NotificationService.cs`, `NotificationsController.cs`, `Scripts/notifications.js` | C/U/D events → JSON on MSMQ; `GetNotifications` does a **destructive** receive of up to 10 messages; JS polls every 5 s and shows toasts | MSMQ, D3, D1 |
| D8 Home and Reporting | `HomeController.cs`, `Views/Home/*` | Landing page; About = student count by enrollment date | D3, D2 |

**Data ownership quirks a rebuild must reproduce or consciously drop:**
- **Enrollment** is written only by the seed. No UI creates, edits or deletes enrollments.
- The **Notification** table is mapped but never read or written. Notifications exist only in MSMQ.
- Deleting an instructor nulls out `Department.InstructorID` (`InstructorsController.cs:236-242`).
- The first browser tab to poll consumes each notification, so other admins never see it.

## Production Runtime Profile

No telemetry available. There is no APM, no logs and no runtime exports (PREFLIGHT Check 5). Runtime cost and variance per domain are unknown. One structural signal stands out: every request (including Home/About) opens an MSMQ handle and may create the queue, and each `GetNotifications` poll can block for 1 s or more per message.

## Technical Debt (top 10, by remediation value)

| # | Debt | Evidence | Why it matters | Remediation |
|---|---|---|---|---|
| 1 | MSMQ notification service | `Services/NotificationService.cs:2,20-23,74`; `BaseController.cs:12` | `System.Messaging` does not exist on .NET 5+; this is a hard blocker. The queue is created per request with Everyone: FullControl | `INotificationPublisher` interface + outbox table / Service Bus / SignalR; create the queue at deploy time, not at runtime |
| 2 | System.Web / MVC 5 app model | `Global.asax.cs:12-19`; `App_Start/BundleConfig.cs`; `HttpPostedFileBase` `CoursesController.cs:47,130`; `Server.MapPath` `:76,159,172,229` | None of these exist in ASP.NET Core | `Program.cs`, `IFormFile`, `IWebHostEnvironment`, static files / Vite |
| 3 | EF Core 3.1.32 + Extensions 3.1 are EOL (Dec 2022) | `packages.config:17-33` | No security patches. 3.1 is the last EF Core on .NET Framework, so the framework and EF upgrades must happen together | EF Core 10 on .NET 10; re-check query translation |
| 4 | No DI; base class builds its own dependencies | `BaseController.cs:11-17`; duplicated setup in `Global.asax.cs:27-29` and `SchoolContextFactory.cs:10`; inconsistent `Dispose` overrides | Untestable; it is also the natural seam for the port | `AddDbContext`, constructor injection |
| 5 | `EnsureCreated()` instead of migrations | `Data/DbInitializer.cs:12` | Cannot evolve an existing schema. Model changes such as `TeachingMaterialImagePath` silently do nothing on an existing database | Initial migration as a baseline; idempotent seeder |
| 6 | Swallowed exceptions, `Debug.WriteLine` "logging" | `BaseController.cs:31-35`; `NotificationService.cs:63-67,83-87`; `InstructorsController.cs:168`; empty `Services/LoggingService.cs` | Production failures are invisible; lost notifications are silent | `ILogger<T>`, structured logging, ProblemDetails |
| 7 | Duplicated upload and notification code | Upload block copied in `CoursesController.cs:52-96` and `:135-189`; 12 notification call sites; date check duplicated in `StudentsController.cs:98-107,152-161`. Edit deletes the old file *before* saving the new one (`:170-180`) | Fixes must be made twice; local disk fails on scale-out or containers | `IFileStorage` + one validator; SaveChanges interceptor / domain events |
| 8 | `.Single()` followed by dead null checks; unguarded `Find()` | `CoursesController.cs:29,210,224`; `StudentsController.cs:72,206`; `InstructorsController.cs:30-37,107,154,232`; `int.Parse` `:77` | A missing ID returns 500, not 404; `Instructors/Index?courseID=X` without `id` throws a NullReferenceException | `SingleOrDefault` + `NotFound()`, `TryParse`. These are quirks to record as rules before deciding to keep or fix them |
| 9 | Dead and misleading code | `LoggingService.cs` (0 bytes); no-op `MarkAsRead` returns success (`NotificationService.cs:90-94`); unused `Notification` table; `HomeController.Unauthorized` has no view; `ErrorViewModel` unused; auth comments with no auth behind them | Misleads whoever ports it | Delete or implement; correct the comments |
| 10 | No tests, sync-only I/O, hardcoded config, project/disk drift | No test project; no `async` anywhere; 5 MB limit in code vs 10 MB in `Web.config:31,38`; page size hardcoded `StudentsController.cs:57`; `DateTime.Now` `NotificationService.cs:49`; notification view/JS/CSS **not in the csproj** (an MSBuild publish would omit them); csproj lists ~10 missing files | No regression safety net for a rewrite | Characterization tests first; `IOptions<T>`; `UtcNow`; reconcile files |

Correction to subagent output: the debt scan said no script polls `GetNotifications`. That is wrong. `Scripts/notifications.js:28,36` polls `/Notifications/GetNotifications` every 5 s, and `_Layout.cshtml:39` loads it on every page.

## Security Findings

**No credentials found.** The only connection string (`Web.config:11`) uses LocalDB with Integrated Security; no password, key or token appears anywhere. No `SECRETS.local.md` was needed.

22 findings: 2 Critical, 4 High, 8 Medium, 8 Low. No automated CVE scanner could run (`packages.config` projects don't support `dotnet list package --vulnerable`); dependency findings come from the manifest, the version banners in the shipped JS, and the NU1903 restore warning. SEC-001, SEC-002 and SEC-006 were re-checked against the source for this report.

| # | Sev | CWE | Finding | file:line |
|---|---|---|---|---|
| SEC-001 | **Critical** | CWE-306, CWE-862 | No authentication or authorization anywhere; all CRUD and the "admin" feed are anonymous | `App_Start/FilterConfig.cs:11`, `Controllers/BaseController.cs:28` |
| SEC-002 | **Critical** | CWE-22, CWE-73, CWE-915 | `TeachingMaterialImagePath` is bindable from the form, then passed to `Server.MapPath` → `File.Delete`. Any visitor can delete `~/Web.config` or `~/bin/*.dll` | `Controllers/CoursesController.cs:47,130,170-176,227-235`; `Views/Courses/Edit.cshtml:64` |
| SEC-003 | High | CWE-79 | Stored DOM XSS: `notifications.js` writes `Message`/`EntityType`/`CreatedBy` with `innerHTML`, on every page | `Scripts/notifications.js:80-84` |
| SEC-004 | High | CWE-732 | MSMQ queue created with Everyone: FullControl (anyone can forge, read or purge messages) | `Services/NotificationService.cs:22-23` |
| SEC-005 | High | CWE-1104 | Microsoft.Data.SqlClient 2.1.4: CVE-2024-0056 / GHSA-98g6-xh36-x2p7 (TDS encryption bypass, MITM) | `packages.config:14` |
| SEC-006 | High | CWE-1104, CWE-79 | jQuery actually shipped is 3.4.1 (CVE-2020-11022/11023); the manifest says 3.7.1 | `Scripts/jquery-3.4.1.js`; `App_Start/BundleConfig.cs:9-10` |
| SEC-007 | Med | CWE-1104, CWE-79 | Bootstrap JS shipped is 3.4.1 (EOL, CVE-2024-6485); the manifest says 5.3.3 | `Scripts/bootstrap.js:1` |
| SEC-008 | Med | CWE-1333, CWE-79 | jquery.validate 1.17.0 (ReDoS CVEs, CVE-2025-3573); the "unobtrusive" file is actually a copy of validate | `Scripts/jquery.validate.js:2`, `Scripts/jquery.validate.unobtrusive.js:1` |
| SEC-009 | Med | CWE-1104 | Microsoft.Identity.Client 4.21.1: CVE-2024-35255 (transitive via SqlClient) | `packages.config:16` |
| SEC-010 | Med | CWE-1104 | EF Core / Extensions 3.1.32 are EOL; Caching.Memory is likely in the CVE-2024-43483 range (unconfirmed) | `packages.config:17-33` |
| SEC-011 | Med | CWE-434 | Upload checked by extension only; files stored under the web root and served unauthenticated, with no `nosniff` header | `Controllers/CoursesController.cs:55-58,76-87,138-141` |
| SEC-012 | Med | CWE-650, CWE-200 | `GetNotifications` is an unauthenticated, destructive GET that returns PII; anyone (or a cross-site `<img>`) can drain the queue | `Controllers/NotificationsController.cs:12-41` |
| SEC-013 | Med | CWE-489, CWE-209 | `compilation debug="true"`, no `customErrors`; `ex.Message` (with server paths) shown to users | `Web.config:30`; `Views/Shared/Error.cshtml:10-14`; `CoursesController.cs:92,185` |
| SEC-014 | Med | CWE-400 | `executionTimeout=3600` + 10 MB bodies + no auth → slow-upload resource exhaustion | `Web.config:31,38` |
| SEC-015 | Low | CWE-352 | `MarkAsRead` POST has no `[ValidateAntiForgeryToken]` (currently a no-op) | `Controllers/NotificationsController.cs:44-57` |
| SEC-016 | Low | CWE-693, CWE-1021 | No security headers (CSP, XFO, nosniff, HSTS); version headers not removed; no cookie flags | `Web.config:29-41` |
| SEC-017 | Low | CWE-601 | Overposted image path can point to an external URL rendered in `<img src>` (tracking) | `Views/Courses/Index.cshtml:50`, `Details.cshtml:43` |
| SEC-018 | Low | CWE-915 | Nested `OfficeAssignment` bind exposes its key to overposting | `Controllers/InstructorsController.cs:70,149-150` |
| SEC-019 | Low | CWE-20, CWE-248 | `int.Parse`, `.Single()`, unguarded `Find()` → unhandled 500s | `InstructorsController.cs:77,107,232`; `CoursesController.cs:29,224`; `StudentsController.cs:206` |
| SEC-020 | Low | CWE-1068 | Comments and UI claim role-based access ("Only admins can delete") that does not exist | `InstructorsController.cs:224`; `StudentsController.cs:14,62`; `Views/Notifications/Index.cshtml:82` |
| SEC-021 | Low | CWE-532 | Student names (PII) and stack traces written to Trace | `Controllers/StudentsController.cs:123,177` |
| SEC-022 | Low | CWE-502 | Untrusted queue messages are deserialized (not RCE: string formatter, `TypeNameHandling.None`) | `Services/NotificationService.cs:31,75-76` |

Checked clean: SQL injection (all parameterized LINQ), `Html.Raw` (constant strings only), CSRF on all entity POSTs.

## Documentation Gaps (top 5)

1. **Security model.** `README.md`, `SETUP_TESTING_GUIDE.md` ("uses Windows Authentication… ensure your Windows user is in the administrator role") and `NOTIFICATION_SYSTEM_README.md` ("Admin-only") describe authentication and roles. The code has none: the global `Authorize` is commented out and the user is always `"System"`. A new engineer needs to know the app is fully anonymous, and that `ROLE_SETUP_GUIDE.md` and `Views/Home/Unauthorized` are gone.
2. **Notification delivery semantics.** The docs promise "reliable, guaranteed delivery" to administrators. In reality, each message is consumed by whichever browser polls first, send failures are swallowed, `MarkAsRead` does nothing, the `Notification` table is never used, and toasts last 60 s (the dashboard says 8 s). Nothing documents that every request opens or creates the queue, so **the whole site fails if MSMQ is not installed**: the `NotificationService` constructor is not inside a try/catch.
3. **Database lifecycle.** `README.md` says the initializer "handles model changes by recreating the database". It does not: `EnsureCreated()` never alters or recreates an existing database, so schema changes require a manual drop. Nothing describes the TPH `Person` table, the `datetime2` convention, or that Enrollment is seed-only.
4. **Upload behavior and limits.** `TEACHING_MATERIAL_UPLOAD.md` calls storage "secure" and the filename "unique". It doesn't mention that the stored path is client-controlled (SEC-002), that the code limit (5 MB) and the `Web.config` limit (10 MB) differ, that Edit deletes the old file before saving the new one, or that uploads need a writable folder under the web root.
5. **Build and deploy reality.** The README targets "4.8.2" and Visual Studio 2019. Nothing says that the shipped JS libraries differ from `packages.config`, that notification assets and the view are missing from the csproj (an MSBuild publish would drop them), or that the .NET Framework 4.8 targeting pack is required (PREFLIGHT 3b). There is also no description of the startup order or error handling conventions.

## Relative Scale

| Metric | Value |
|---|---|
| First-party KSLOC | 4.0 |
| Complexity index (`2.94 × KSLOC^1.10`) | **13.5** |

The index is a relative size measure for ranking this system against others measured the same way. **It is not a timeline or a cost**, and it assumes human-team productivity that does not apply to agentic modernization. On any portfolio scale, this is a very small system.

## Recommended Modernization Pattern

**Rebuild → `/code-modernization:modernize-reimagine contoso`**

The stated target in `INTENT.md` is a different architecture: a .NET 10 REST API container plus a React 19 SPA container, organized as Clean Architecture vertical slices by bounded context. That replaces the server-rendered Razor UI, the System.Web host, the per-request MSMQ coupling and the controller-owned data access, so this is a rebuild, not an uplift. An in-place `uplift` to ASP.NET Core MVC would still need every controller, view, the upload path and the messaging layer rewritten, and would still leave the UI split undone. The codebase is small (4 KSLOC, 8 domains that map cleanly to bounded contexts: Students, Courses/Materials, Faculty/Departments, Notifications, Reporting), so rebuilding from extracted intent is cheaper than translating code.

The constraint is that **behavior must match exactly, including quirks**. That makes rule extraction and characterization tests a precondition, not an option. Several "quirks" here are security defects (anonymous writes, the file-delete overposting, destructive notification reads, 500-instead-of-404 errors). Each one needs an explicit keep-or-fix decision recorded in `/code-modernization:modernize-review` before the build, not a silent change during it.

Suggested order: `modernize-map` → `modernize-extract-rules` → `modernize-review` (decide on the security quirks) → `modernize-brief` → `modernize-reimagine`. Run `modernize-harden` only if the legacy app stays in production during the rebuild; SEC-001 and SEC-002 are worth a hotfix in that case.
