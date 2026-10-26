# Business Rules — contoso

At extraction: 49 confirmed rules (2 P0); later steps may add or correct rules below. Each citation was checked by a second agent that read the cited lines; 2 candidate rules were refuted and left out.

| ID | Name | Category | Priority | Source | Confidence |
|---|---|---|---|---|---|
| RULE-001 | Student enrollment statistics by enrollment date | Calculation | P1 | `Controllers/HomeController.cs:16-27` | High |
| RULE-002 | Paged result window and page count | Calculation | P1 | `PaginatedList.cs:12-29` | High |
| RULE-003 | Full name display format | Calculation | P2 | `Models/Person.cs:21-28` | High |
| RULE-004 | Relative time display ('time ago') | Calculation | P2 | `Scripts/notifications.js:123-139` | High |
| RULE-005 | Notification message wording | Calculation | P2 | `Services/NotificationService.cs:96-113` | High |
| RULE-006 | Department edits use optimistic concurrency (first save wins) | Validation | P0 | `Controllers/DepartmentsController.cs:81-134` | Medium |
| RULE-007 | Teaching material image upload acceptance (type and size) | Validation | P1 | `Controllers/CoursesController.cs:52-71` | Medium |
| RULE-008 | Department create/edit field rules | Validation | P1 | `Controllers/DepartmentsController.cs:45-60` | Medium |
| RULE-009 | Instructor create requires a valid hire date | Validation | P1 | `Controllers/InstructorsController.cs:68-93` | High |
| RULE-010 | Student enrollment date must be a real date within the 1753-9999 range | Validation | P1 | `Controllers/StudentsController.cs:97-107` | Medium |
| RULE-011 | Duplicate enrollment prevention (one enrollment per student per course) during… | Validation | P1 | `Data/DbInitializer.cs:238-248` | Medium |
| RULE-012 | Instructor can be assigned to a given course at most once (many-to-many teachin… | Validation | P1 | `Data/SchoolContext.cs:55-68` | Medium |
| RULE-013 | Course record field constraints | Validation | P1 | `Models/Course.cs:9-23` | High |
| RULE-014 | Department name length 3-50 characters (but not required) | Validation | P1 | `Models/Department.cs:12-13` | Medium |
| RULE-015 | Enrollment grade scale A-F, optional | Validation | P1 | `Models/Enrollment.cs:5-16` | High |
| RULE-016 | Instructor hire date is required and must fall within 1753-9999 | Validation | P1 | `Models/Instructor.cs:10-16` | High |
| RULE-017 | Instructor has at most one office; office location max 50 chars | Validation | P1 | `Models/OfficeAssignment.cs:8-12` | High |
| RULE-018 | Person name is required and limited to 50 characters | Validation | P1 | `Models/Person.cs:10-19` | High |
| RULE-019 | Student identity fields are required and length-limited | Validation | P1 | `Models/Person.cs:10-19` | Medium |
| RULE-020 | Maximum request/upload size of 10 MB | Validation | P1 | `Web.config:31-38` | Medium |
| RULE-021 | Course lookup requires an id and an existing course | Validation | P2 | `Controllers/CoursesController.cs:23-34` | High |
| RULE-022 | Missing student id handling on detail/edit/delete views | Validation | P2 | `Controllers/StudentsController.cs:63-78` | High |
| RULE-023 | Client-side validation enabled | Validation | P2 | `Web.config:16-17` | High |
| RULE-024 | Image replacement on course edit removes previous file | Lifecycle | P1 | `Controllers/CoursesController.cs:165-181` | High |
| RULE-025 | Course deletion removes its image and the course | Lifecycle | P1 | `Controllers/CoursesController.cs:221-251` | Medium |
| RULE-026 | Course change notifications | Lifecycle | P1 | `Controllers/CoursesController.cs:98-102` | High |
| RULE-027 | Instructor course assignments are synchronized to the selected course set | Lifecycle | P1 | `Controllers/InstructorsController.cs:177-207` | High |
| RULE-028 | Deleting an instructor unassigns them as department administrator | Lifecycle | P1 | `Controllers/InstructorsController.cs:227-250` | Medium |
| RULE-029 | Student record lifecycle with change notifications | Lifecycle | P1 | `Controllers/StudentsController.cs:109-119` | Medium |
| RULE-030 | One-time reference data seeding gated on existence of any student | Lifecycle | P1 | `Data/DbInitializer.cs:9-18` | High |
| RULE-031 | Notification creation on entity change (fire-and-forget) | Lifecycle | P1 | `Services/NotificationService.cs:39-68` | High |
| RULE-032 | Mark-as-read is a no-op (IsRead/ReadAt lifecycle not implemented) | Lifecycle | P1 | `Services/NotificationService.cs:90-94` | High |
| RULE-033 | No authentication or authorization required for any page | Policy | P0 | `App_Start/FilterConfig.cs:7-12` | High |
| RULE-034 | Change notifications are attributed to 'System' and are best-effort | Policy | P1 | `Controllers/BaseController.cs:19-36` | High |
| RULE-035 | Teaching material image storage and naming | Policy | P1 | `Controllers/CoursesController.cs:73-95` | High |
| RULE-036 | Blank office location removes the instructor's office assignment | Policy | P1 | `Controllers/InstructorsController.cs:149-157` | High |
| RULE-037 | Delete authorization stated in comments is not enforced | Policy | P1 | `Controllers/InstructorsController.cs:224-227` | Low |
| RULE-038 | Notification retrieval is destructive and capped at 10 per poll | Policy | P1 | `Controllers/NotificationsController.cs:13-41` | Medium |
| RULE-039 | Student screens intended for Admins and Teachers but not enforced | Policy | P1 | `Controllers/StudentsController.cs:14-15` | Low |
| RULE-040 | Only name and enrollment date may be set from the student form | Policy | P1 | `Controllers/StudentsController.cs:93` | High |
| RULE-041 | Person stored as a single table, with Student/Instructor role set by a discrimi… | Policy | P1 | `Data/SchoolContext.cs:47-53` | High |
| RULE-042 | Course numbers are business-assigned, not auto-generated | Policy | P1 | `Models/Course.cs:9-11` | Medium |
| RULE-043 | Department administrator is optional and must be an instructor | Policy | P1 | `Models/Department.cs:24-29` | Medium |
| RULE-044 | Default landing page and URL scheme | Policy | P2 | `App_Start/RouteConfig.cs:8-17` | High |
| RULE-045 | Change notifications on instructor and department create/update/delete | Policy | P2 | `Controllers/DepartmentsController.cs:151-165` | High |
| RULE-046 | Instructor directory drill-down (instructor to courses to enrollments) | Policy | P2 | `Controllers/InstructorsController.cs:16-41` | High |
| RULE-047 | Student list search, sort and paging | Policy | P2 | `Controllers/StudentsController.cs:15-59` | High |
| RULE-048 | New student defaults to today's enrollment date | Policy | P2 | `Controllers/StudentsController.cs:81-88` | High |
| RULE-049 | Department has budget, start date and optional administrator instructor | Policy | P2 | `Data/DbInitializer.cs:66-86` | Medium |

## Calculation

### RULE-001: Student enrollment statistics by enrollment date
**Category:** Calculation
**Priority:** P1
**Source:** `Controllers/HomeController.cs:16-27`
**Plain English:** The About page reports how many students enrolled on each distinct enrollment date, computed by counting all students that share that date.
**Specification:**
  Given Student records: 3 enrolled 2005-09-01, 1 enrolled 2002-09-01, 2 enrolled 2003-09-01 (all with time 00:00:00)
  When  A user opens the Home/About page
  Then  The page shows three rows: 2005-09-01 = 3, 2002-09-01 = 1, 2003-09-01 = 2 (StudentCount = COUNT(students) GROUP BY EnrollmentDate). The output is not explicitly sorted, so the database decides the row order.
**Parameters:** Grouping key: Student.EnrollmentDate (datetime2, non-nullable, see Models/Student.cs:14-16). Aggregate: count of students per key. Output shape: EnrollmentDateGroup {EnrollmentDate (shown as date only), StudentCount} (Models/SchoolViewModels/EnrollmentDateGroup.cs:6-12). No filters: every student is counted, regardless of status or whether they have enrollments.
**Edge cases handled:** The grouping uses the full datetime value, including the time. Two students enrolled on the same day at different times count as separate groups, but both rows show the same date because the view mod…; No students: the result is an empty list.; No ORDER BY: the row order is not guaranteed.; EnrollmentDateGroup.EnrollmentDate is nullable, but the source column is non-nullable, so a null group cannot happen in practice.
**Suspected defect:** Grouping by the full datetime2 value instead of its date part can split one calendar day into several rows that look identical. This only matters if enrollment dates are ever saved with a time part. Also, the rows have no defined order.
**Confidence:** High

### RULE-002: Paged result window and page count
**Category:** Calculation
**Priority:** P1
**Source:** `PaginatedList.cs:12-29`
**Plain English:** List screens show one page of records at a time. Page numbers start at 1. The total page count is the record count divided by the page size, rounded up, and Previous/Next navigation is offered only when such a page exists.
**Specification:**
  Given A query that returns 23 matching records, page size 10, and requested page 3
  When  The paginated list is built
  Then  10 records are skipped ((3-1) x 10 = 20), records 21 to 23 are returned (3 items), TotalPages = ceil(23/10) = 3, HasPreviousPage = true (3 > 1), and HasNextPage = false (3 is not less than 3)
**Parameters:** Pages start at 1. Skip = (pageIndex - 1) x pageSize. Take = pageSize. TotalPages = ceiling(count / pageSize). HasPreviousPage = pageIndex > 1. HasNextPage = pageIndex < TotalPages. The page size is supplied by the caller and is not set in this file.
**Edge cases handled:** 0 records: TotalPages = 0, HasNextPage = false, and HasPreviousPage = false on page 1; A page number beyond TotalPages returns an empty item list. HasPreviousPage is then true and HasNextPage is false.; Page index 0 or a negative value gives a negative Skip offset. The code does not check for this, and the query provider decides what happens.; Page size 0: count/0.0 gives Infinity or NaN, and casting that to int gives an undefined or implementation-specific TotalPages. The code does not check for this.; The total count and the page of items come from two separate queries, so they can disagree if the data changes between the two calls
**Suspected defect:** The code does not check that pageIndex >= 1 or pageSize > 0. With a page size of 0, TotalPages comes from casting Infinity or NaN to int.
**Confidence:** High

### RULE-003: Full name display format
**Category:** Calculation
**Priority:** P2
**Source:** `Models/Person.cs:21-28`
**Plain English:** A person's full name is shown as last name, a comma and a space, then first name.
**Specification:**
  Given LastName 'Alexander' and FirstMidName 'Carson'
  When  FullName is read
  Then  The result is 'Alexander, Carson'
**Parameters:** Format: LastName + ", " + FirstMidName
**Edge cases handled:** A null name gives an empty part, for example ', Carson'. Validation normally prevents this.; FullName is computed when read and is not stored
**Confidence:** High

### RULE-004: Relative time display ('time ago')
**Category:** Calculation
**Priority:** P2
**Source:** `Scripts/notifications.js:123-139`
**Plain English:** How long ago a notification was created is shown as 'just now', or in whole minutes, hours or days, rounded down and pluralized.
**Specification:**
  Given A notification created 7,250 seconds ago
  When  It is displayed
  Then  It shows '2 hours ago' (floor(7250/3600)=2). Under 60s shows 'just now', under 3600s shows minutes, under 86400s shows hours, otherwise days.
**Parameters:** Thresholds: 60 s, 3600 s, 86400 s; always rounds down
**Edge cases handled:** Exactly 1 unit is singular ('1 minute ago'); Server CreatedAt is local time without a zone, so client time zone differences can skew the result or make it negative (negative shows 'just now')
**Confidence:** High

### RULE-005: Notification message wording
**Category:** Calculation
**Priority:** P2
**Source:** `Services/NotificationService.cs:96-113`
**Plain English:** The notification text names the entity by its display name when one is given, otherwise by its ID, and is worded according to the operation.
**Specification:**
  Given EntityType 'Course' with display name 'Calculus' (or ID 1050 when no name is given)
  When  The operation is CREATE, UPDATE or DELETE
  Then  CREATE -> "New Course 'Calculus' has been created"; UPDATE -> "Course 'Calculus' has been updated"; DELETE -> "Course (ID: 1050) has been deleted" when no name is given
**Parameters:** Templates: 'New {x} has been created', '{x} has been updated', '{x} has been deleted', fallback '{x} operation: {op}'
**Edge cases handled:** A blank or whitespace display name falls back to '(ID: id)'; Any other operation value uses the fallback template
**Confidence:** High

## Validation

### RULE-006: Department edits use optimistic concurrency (first save wins)
**Category:** Validation
**Priority:** P0
**Source:** `Controllers/DepartmentsController.cs:81-134`
**Also cited:** Models/Department.cs:26-27
**Plain English:** A department edit is rejected if someone else changed or deleted the department after the user opened it; the user is shown the current database values for each conflicting field and must save again on purpose to overwrite them.
**Specification:**
  Given User A and User B both open the English department with Budget $350,000.00. User B saves Budget $0.00
  When  User A saves Budget $400,000.00 using the old RowVersion
  Then  The save is cancelled. Budget shows 'Current value: $0.00' next to the field along with the general 'modified by another user' message, and the form's RowVersion is updated to the database value so that a second save succeeds
**Parameters:** The concurrency token is RowVersion ([Timestamp] on Department). The fields compared are Name, Budget (shown as currency), StartDate (shown as a short date) and InstructorID (shown as the instructor's full name).
**Edge cases handled:** The department was deleted by another user: error 'Unable to save changes. The department was deleted by another user.'; The administrator changed to null in the database: the message shows a blank current value; Model validation fails: no save is attempted and the form is shown again
**Confidence:** Medium — P0 panel doubts spec fidelity: Most of the card matches the code. Department.RowVersion has a [Timestamp] attribute (Models/Department.cs:26-27), so EF throws DbUpdateConcurrencyException when a save uses a stale token. Controllers/DepartmentsController.cs:96-128 handles it this way. If the row was deleted, it shows the 'deleted by another user' message. Otherwise it compares Name, Budget, StartD…

### RULE-007: Teaching material image upload acceptance (type and size)
**Category:** Validation
**Priority:** P1
**Source:** `Controllers/CoursesController.cs:52-71`
**Plain English:** An optional teaching-material image may be attached to a course only if its file extension is jpg, jpeg, png, gif or bmp and it is no larger than 5 MB; otherwise the whole course save is rejected with an error.
**Specification:**
  Given A valid course form with an attached file "syllabus.pdf" (or "photo.png" of 6,000,000 bytes)
  When  The course is created or edited
  Then  The form is redisplayed with error "Please upload a valid image file (jpg, jpeg, png, gif, bmp)." (or "File size must be less than 5MB.") and the course is NOT saved. A "photo.PNG" of 5,242,880 bytes is accepted.
**Parameters:** Allowed extensions: .jpg, .jpeg, .png, .gif, .bmp (case-insensitive via ToLower); Max size 5 * 1024 * 1024 = 5,242,880 bytes (inclusive). Same logic duplicated in Edit at CoursesController.cs:135-154
**Edge cases handled:** No file or zero-length file: upload skipped, course saved without changing image; Size check uses '>' so exactly 5 MB is accepted although the message says 'less than 5MB'; Only the file name extension is checked; content/MIME type is not inspected; Validation only runs after model validation passes
**Suspected defect:** Type check relies solely on the client-supplied file name extension; a non-image file renamed to .jpg is accepted and stored under the web root.
**Confidence:** Medium — P0 panel split on whether this is critical to the system's core purpose or a costly-if-wrong rule (The rule card matches the code. In legacy/contoso/Controllers/CoursesController.cs, lines 52-71 (Create) and 135-154 (Edit) only check a file when one is attached and is not empty (ContentLength > 0). The extension is lower-cased with ToLower, so the check ignores case, and it must be one of .jpg, .…

### RULE-008: Department create/edit field rules
**Category:** Validation
**Priority:** P1
**Source:** `Controllers/DepartmentsController.cs:45-60`
**Plain English:** A department is saved only if its data passes validation: the name must be 3 to 50 characters, the budget is a money amount, a start date is required, and an administrator (instructor) is optional.
**Specification:**
  Given A new department with Name 'IT', Budget 100000 and Start Date 2026-09-01
  When  The department create form is submitted
  Then  Validation fails because the name is shorter than 3 characters, and the form is shown again with the instructor dropdown keeping the selected value
**Parameters:** Name length 3-50 characters (Department model StringLength). Budget is stored as a SQL money column. Only the fields Name, Budget, StartDate and InstructorID can be bound on Create; Edit also binds DepartmentID and RowVersion.
**Edge cases handled:** InstructorID null: allowed, so the department has no administrator; Budget has no range check, so negative values are accepted; Name is not marked [Required], so an empty name may pass validation
**Suspected defect:** Negative budgets are not blocked, and an empty department name may be accepted.
**Confidence:** Medium — Should the department budget have a minimum (for example >= 0) or a maximum, and should the department name be required? Neither is enforced today.

### RULE-009: Instructor create requires a valid hire date
**Category:** Validation
**Priority:** P1
**Source:** `Controllers/InstructorsController.cs:68-93`
**Plain English:** A new instructor is saved only when their data is valid, including a required hire date between 1 Jan 1753 and 31 Dec 9999; after a successful save, a creation notification is sent.
**Specification:**
  Given A new instructor 'Kapoor, Candace' with HireDate 1700-01-01 and course 1045 selected
  When  The instructor create form is submitted
  Then  Validation fails with 'Hire date must be between 1753 and 9999'. Nothing is saved, and the course checklist is shown again with 1045 ticked
**Parameters:** Hire date range 1/1/1753 to 12/31/9999 (Instructor model). Bindable fields: LastName, FirstMidName, HireDate, OfficeAssignment. Name rules come from the Person base class.
**Edge cases handled:** Valid data: the instructor and course assignments are saved, a CREATE notification is sent, and the user is redirected to Index
**Confidence:** High

### RULE-010: Student enrollment date must be a real date within the 1753-9999 range
**Category:** Validation
**Priority:** P1
**Source:** `Controllers/StudentsController.cs:97-107`
**Plain English:** A student cannot be saved (created or edited) unless the enrollment date is supplied and falls between 1 Jan 1753 and 31 Dec 9999.
**Specification:**
  Given A registrar enters a new student 'Ana Lopez' with enrollment date left blank (binds to 0001-01-01)
  When  The Create (or Edit) form is submitted
  Then  The save is refused with 'Please enter a valid enrollment date.' and 'Enrollment date must be between 1753 and 9999.' on the EnrollmentDate field, and the form is redisplayed; with enrollment date 2024-09-01 the student is saved
**Parameters:** Lower bound 1753-01-01 (SQL Server legacy datetime minimum); upper bound 9999-12-31 00:00; same check duplicated in Edit at StudentsController.cs:151-161; also declared as [Required] and [Range(typeof(DateTime), "1/1/1753", "12/31/9999")] in Models/Student.cs:10-16 (column type datetime2)
**Edge cases handled:** DateTime.MinValue / default date triggers both error messages at once (the MinValue check is redundant with the range check); Upper bound compared as 9999-12-31 00:00, so any time later on that last day is rejected; No business limit on future dates or dates before the university existed - e.g. 1800-01-01 or 2099-01-01 are accepted; Range is a technical storage limit, not a business rule; column is datetime2 so the 1753 floor may be unnecessary
**Confidence:** Medium — P0 panel split on whether this is critical to the system's core purpose or a costly-if-wrong rule (The rule card matches the code, but this rule should not be P0. Faithful: StudentsController.cs:97-107 (Create) adds the error "Please enter a valid enrollment date." when EnrollmentDate is DateTime.MinValue or default. It adds "Enrollment date must be between 1753 and 9999." when the date is before…

### RULE-011: Duplicate enrollment prevention (one enrollment per student per course) during seeding
**Category:** Validation
**Priority:** P1
**Source:** `Data/DbInitializer.cs:238-248`
**Plain English:** An enrollment is added only if the same student is not already enrolled in the same course.
**Specification:**
  Given Student Alexander is already enrolled in course 1050 Chemistry
  When  The seeder tries to add another Alexander/Chemistry enrollment
  Then  The duplicate is skipped and only enrollments for new student+course pairs are saved
**Parameters:** Uniqueness key: (StudentID, CourseID)
**Edge cases handled:** The check is in application code only. SchoolContext declares no unique index on Enrollment(StudentID, CourseID), so other write paths are not protected at the database level; SingleOrDefault throws if more than one matching row already exists
**Confidence:** Medium — Is 'a student can enroll in a course only once' a real business rule? If so, should it be a database unique constraint (it currently exists only in the seeder), and what about students retaking a course?

### RULE-012: Instructor can be assigned to a given course at most once (many-to-many teaching assignment)
**Category:** Validation
**Priority:** P1
**Source:** `Data/SchoolContext.cs:55-68`
**Also cited:** Data/SchoolContext.cs:55-57 (composite key); Controllers/InstructorsController.cs:177-207 (add/remove without duplicates)
**Plain English:** A course can have many instructors and an instructor can teach many courses, but each instructor-course pair can be recorded only once.
**Specification:**
  Given Instructor Kapoor is already assigned to Chemistry (1050)
  When  A second Kapoor/Chemistry assignment is saved
  Then  The save fails on a primary-key violation; assignments of other instructors (e.g. Harui) to Chemistry succeed
**Parameters:** Composite key (CourseID, InstructorID); FKs to Course.CourseID and Person(Instructor).ID
**Edge cases handled:** Seed data co-assigns Chemistry to Kapoor and Harui; Zheng teaches both Micro- and Macroeconomics
**Confidence:** Medium — Citation was corrected by referee (Models/CourseAssignment.cs:8-14 is only a plain join-entity POCO: InstructorID, CourseID and two navigation properties. It has no [Key] attribute, no index and no logic, so it does not enforce uniqueness itself. The rule is real but lives elsewhere. Data/SchoolContext.cs:55-57 sets the composite primary key HasKey(c => new { c.CourseID, c.InstructorID }), which…

### RULE-013: Course record field constraints
**Category:** Validation
**Priority:** P1
**Source:** `Models/Course.cs:9-23`
**Plain English:** A course must have a title of 3 to 50 characters, a credit value from 0 to 5, a course number entered by the user (not generated by the system), and a teaching-material image path no longer than 255 characters.
**Specification:**
  Given A user submits a new or edited course with Title "Ch" (2 chars) and Credits 6
  When  The Create or Edit form is posted and model validation runs (CoursesController.cs:49 / :132)
  Then  ModelState is invalid; the course is not saved, the form is redisplayed with the department dropdown re-populated. A course with Title "Chemistry" and Credits 3 passes.
**Parameters:** Title length min 3, max 50; Credits range 0..5 inclusive; TeachingMaterialImagePath max 255 chars; CourseID DatabaseGeneratedOption.None (user-supplied, shown as "Number")
**Edge cases handled:** Title is not marked [Required]; a null/empty title may pass StringLength validation (StringLength ignores null); Credits 0 is allowed; CourseID is user-entered; duplicate course numbers are not checked in the controller and would fail at the database primary-key constraint; DepartmentID has no explicit validation; non-existent department would fail at FK level; Validation failure path at CoursesController.cs:107-108 and :199-200
**Confidence:** High

### RULE-014: Department name length 3-50 characters (but not required)
**Category:** Validation
**Priority:** P1
**Source:** `Models/Department.cs:12-13`
**Plain English:** A department name, when given, must be at least 3 and at most 50 characters.
**Specification:**
  Given A department being created or edited
  When  Name is entered as 'IT' (2 chars) or a 51-character string
  Then  Validation fails and the department is not saved; 'English' passes
**Parameters:** Name MinLength = 3; Name MaxLength = 50
**Edge cases handled:** No [Required] attribute: a null/empty name passes StringLength validation; Budget has no range constraint (negative budgets accepted); stored as SQL money; StartDate has no range validation, unlike Instructor.HireDate
**Suspected defect:** Department Name is not marked Required, so a department can be saved with no name; Budget accepts negative values.
**Confidence:** Medium — Should a department name be mandatory, and should Budget be constrained to non-negative values? The current model allows a blank name and any budget amount.

### RULE-015: Enrollment grade scale A-F, optional
**Category:** Validation
**Priority:** P1
**Source:** `Models/Enrollment.cs:5-16`
**Also cited:** Data/DbInitializer.cs:212-215
**Plain English:** An enrollment links one student to one course and may carry a letter grade of A, B, C, D or F; a missing grade is shown as 'No grade'.
**Specification:**
  Given Student Alexander enrolled in course 1050 with no grade yet
  When  The student's details are displayed
  Then  The enrollment shows 'No grade'; once graded, only A, B, C, D or F are valid
**Parameters:** Grade enum: A, B, C, D, F (no +/- or pass/fail, no E); Grade nullable; NullDisplayText 'No grade'
**Edge cases handled:** No GPA or credit calculation exists in these files; No uniqueness constraint here preventing the same student enrolling twice in the same course (DbInitializer de-duplicates seed data only)
**Confidence:** High

### RULE-016: Instructor hire date is required and must fall within 1753-9999
**Category:** Validation
**Priority:** P1
**Source:** `Models/Instructor.cs:10-16`
**Plain English:** Every instructor must have a hire date, and that date must be between 1 January 1753 and 31 December 9999.
**Specification:**
  Given An instructor record being created or edited
  When  The hire date is missing, or is entered as 1700-06-01
  Then  Validation fails with 'Hire date must be between 1753 and 9999' (or a required-field error) and the record is not saved; a hire date of 2020-08-15 passes
**Parameters:** Min HireDate = 1753-01-01; Max HireDate = 9999-12-31; stored as datetime2; display/edit format yyyy-MM-dd
**Edge cases handled:** Range bounds are parsed from culture-sensitive strings '1/1/1753' and '12/31/9999' (US month/day order); No business check that hire date is not in the future; 1753 lower bound mirrors SQL Server legacy datetime limit even though column is datetime2
**Confidence:** High

### RULE-017: Instructor has at most one office; office location max 50 chars
**Category:** Validation
**Priority:** P1
**Source:** `Models/OfficeAssignment.cs:8-12`
**Also cited:** Data/SchoolContext.cs:70-74
**Plain English:** An instructor may have zero or one office assignment, keyed by the instructor, with an office location of up to 50 characters.
**Specification:**
  Given Instructor #5 with office 'Smith 17'
  When  A second office is assigned or a location over 50 characters is entered
  Then  Only one office per instructor can exist (InstructorID is the primary key); a location over 50 characters fails validation
**Parameters:** Location MaxLength = 50; OfficeAssignment PK = InstructorID (1:1 with Instructor, SchoolContext.cs:71-74)
**Edge cases handled:** On instructor edit, a blank/whitespace location removes the office assignment (InstructorsController.cs:154-156); Office cannot exist without an instructor
**Confidence:** High

### RULE-018: Person name is required and limited to 50 characters
**Category:** Validation
**Priority:** P1
**Source:** `Models/Person.cs:10-19`
**Plain English:** Every person (student or instructor) must have a last name and a first name. Each name can be at most 50 characters.
**Specification:**
  Given A person record with LastName 'Alexander' and a 51-character FirstMidName
  When  The record is validated before it is saved
  Then  Validation fails with the message 'First name cannot be longer than 50 characters.' A missing last name or first name also fails as required. Names of up to 50 characters pass.
**Parameters:** LastName: required, max length 50 (default error message). FirstMidName: required, max length 50 (custom message), stored in the database column 'FirstName'.
**Edge cases handled:** An empty string fails [Required], because empty strings are not allowed by default; No minimum length and no character or format rule is set; Person is abstract, so the rule applies through its subtypes (for example Student and Instructor)
**Confidence:** High

### RULE-019: Student identity fields are required and length-limited
**Category:** Validation
**Priority:** P1
**Source:** `Models/Person.cs:10-19`
**Also cited:** (name required/length rules); Models/Student.cs:8-16 (inheritance and EnrollmentDate)
**Plain English:** Every student must have a last name and a first/middle name, each at most 50 characters, plus an enrollment date.
**Specification:**
  Given A student form with Last Name 'Smith' and First Name left blank
  When  The form is submitted for Create or Edit
  Then  Model validation fails (FirstMidName required) and the student is not saved; a 51-character first name fails with 'First name cannot be longer than 50 characters.'
**Parameters:** LastName: required, max 50 (Models/Person.cs:10-13); FirstMidName: required, max 50, stored in column 'FirstName' (Models/Person.cs:15-19); EnrollmentDate required (Student.cs:10); Student inherits Person (Student.cs:8)
**Edge cases handled:** No minimum length - a single-character name is accepted; No character-set or whitespace-only check; Full name derived for display as 'LastName, FirstMidName' (Person.cs:21-28) whereas notifications use 'FirstMidName LastName'
**Confidence:** Medium — Citation was corrected by referee (The behavior is real, but most of it is not in the cited lines. Models/Student.cs:8-16 only shows that Student inherits from Person (line 8) and puts [Required] on EnrollmentDate (line 10), plus a Range limit of 1753-9999 (line 15) that the rule leaves out. The name checks the rule is mainly about live in Models/Person.cs. LastName is [Required] with [StringLeng…

### RULE-020: Maximum request/upload size of 10 MB
**Category:** Validation
**Priority:** P1
**Source:** `Web.config:31-38`
**Plain English:** Any request body, such as an uploaded file, larger than 10 MB is rejected by the web server, and long requests may run up to one hour.
**Specification:**
  Given A user submits a form with an 11 MB file attachment
  When  The request reaches the server
  Then  The request is rejected (exceeds 10,240 KB / 10,485,760 bytes); a 9 MB upload is accepted
**Parameters:** maxRequestLength=10240 KB (line 31); maxAllowedContentLength=10485760 bytes (line 38); executionTimeout=3600 seconds (line 31)
**Edge cases handled:** Both ASP.NET and IIS limits equal 10 MB; the smaller of the two governs; executionTimeout is only enforced when compilation debug=false; debug=true is currently set (line 30)
**Confidence:** Medium — Is 10 MB the business-mandated maximum file upload size (e.g., for instructor photos/documents), and is the 1-hour execution timeout intentional?

### RULE-021: Course lookup requires an id and an existing course
**Category:** Validation
**Priority:** P2
**Source:** `Controllers/CoursesController.cs:23-34`
**Plain English:** Viewing, editing or deleting a course requires a course number; a missing number returns Bad Request and an unknown course is meant to return Not Found.
**Specification:**
  Given A request for course details with no id (or id 9999 that does not exist)
  When  Details, Edit or Delete (GET) is requested
  Then  No id: HTTP 400. Unknown id on Edit (Find): HTTP 404. Unknown id on Details/Delete: .Single() throws an exception (server error) instead of 404.
**Parameters:** Same pattern at CoursesController.cs:112-124 (Edit) and :204-215 (Delete)
**Edge cases handled:** Details and Delete use .Single(), so the null check is unreachable
**Suspected defect:** Details and Delete GET use Single() rather than SingleOrDefault(), so a non-existent course causes an unhandled exception instead of a 404.
**Confidence:** High

### RULE-022: Missing student id handling on detail/edit/delete views
**Category:** Validation
**Priority:** P2
**Source:** `Controllers/StudentsController.cs:63-78`
**Plain English:** Viewing a student requires an id; no id returns Bad Request and an unknown id should return Not Found.
**Specification:**
  Given A request to Students/Details with id 9999 that does not exist
  When  The details page is requested
  Then  Intended: HTTP 404; actual: Single() throws an exception (server error) before the null check
**Parameters:** No id -> HTTP 400 (lines 65-68, 132-135, 186-189); unknown id -> 404 in Edit/Delete (lines 137-140, 191-194)
**Edge cases handled:** Details eagerly loads enrollments and their courses
**Suspected defect:** Details uses .Single() (line 72) instead of SingleOrDefault(), so the 'not found' branch (line 73-76) is unreachable and unknown ids produce an error instead of 404.
**Confidence:** High

### RULE-023: Client-side validation enabled
**Category:** Validation
**Priority:** P2
**Source:** `Web.config:16-17`
**Plain English:** Form field validation rules are also enforced in the browser before submission, in addition to server checks.
**Specification:**
  Given A user leaves a required field blank on a form
  When  They click submit
  Then  The browser shows the validation message without posting to the server (jquery.validate bundle, BundleConfig.cs:12-13)
**Parameters:** ClientValidationEnabled=true; UnobtrusiveJavaScriptEnabled=true
**Confidence:** High

## Lifecycle

### RULE-024: Image replacement on course edit removes previous file
**Category:** Lifecycle
**Priority:** P1
**Source:** `Controllers/CoursesController.cs:165-181`
**Plain English:** When a course is edited with a new valid image, the previously stored image file is deleted and replaced by the new one; editing without a new image keeps the existing image path.
**Specification:**
  Given Course 1050 whose TeachingMaterialImagePath is ~/Uploads/TeachingMaterials/course_1050_old.png
  When  The course is edited and a new valid image "new.gif" is uploaded
  Then  The old file is deleted from disk (if it exists), the new file is saved as course_1050_<guid>.gif, the path is updated, the course is saved as modified, and an UPDATE notification is sent.
**Parameters:** Old path source: TeachingMaterialImagePath bound from the posted form (Bind Include list at CoursesController.cs:130)
**Edge cases handled:** Old file deleted before the new file is saved; if SaveAs then fails, the course keeps a path pointing to a deleted file; No new image: path from the form (hidden field) is persisted as-is
**Suspected defect:** The 'old' image path is taken from the posted form value, not the database, so a client can supply an arbitrary path (e.g. ~/Web.config) that the server will resolve and delete, or persist an arbitrary path on the course. Old path should be read from the stored record.
**Confidence:** High

### RULE-025: Course deletion removes its image and the course
**Category:** Lifecycle
**Priority:** P1
**Source:** `Controllers/CoursesController.cs:221-251`
**Plain English:** Deleting a course first tries to delete its stored teaching-material image (failures are ignored), then removes the course record and sends a DELETE notification.
**Specification:**
  Given Course 4022 "Microeconomics" with a stored image file
  When  The user confirms deletion
  Then  The image file is deleted best-effort, the course row is removed, SaveChanges runs, and a notification ("Course", "4022", "Microeconomics", DELETE) is sent; user is redirected to the course list.
**Parameters:** No eligibility check before deletion
**Edge cases handled:** Image file delete exception is swallowed (debug output only) and does not block course deletion; No check for existing enrollments or instructor assignments; outcome depends on database cascade/FK rules; Unknown id: Find returns null and course.Title throws (unhandled error instead of 404)
**Suspected defect:** No null check after Find(id) in DeleteConfirmed, so deleting a non-existent course yields a server error rather than Not Found.
**Confidence:** Medium — Should a course with enrollments or instructor assignments be deletable, and if so should its enrollments be removed (cascade) or should the deletion be blocked?

### RULE-026: Course change notifications
**Category:** Lifecycle
**Priority:** P1
**Source:** `Controllers/CoursesController.cs:98-102`
**Plain English:** Every successful course create, update, or delete publishes a notification carrying entity type 'Course', the course number, the course title, and the operation.
**Specification:**
  Given A new course 2021 "Composition" passes validation
  When  It is saved to the database
  Then  SendEntityNotification("Course", "2021", "Composition", CREATE) is sent after SaveChanges; UPDATE fires at CoursesController.cs:195 and DELETE at :249
**Parameters:** Operations: CREATE, UPDATE, DELETE (EntityOperation)
**Edge cases handled:** Notification fires only after a successful database save; Delete notification uses the title captured before removal
**Confidence:** High

### RULE-027: Instructor course assignments are synchronized to the selected course set
**Category:** Lifecycle
**Priority:** P1
**Source:** `Controllers/InstructorsController.cs:177-207`
**Plain English:** When an instructor is edited, the courses they teach become exactly the courses ticked on the form: new ticks add assignments, missing ticks remove them, and if nothing is ticked every assignment is removed.
**Specification:**
  Given Instructor 9 currently teaches courses 1045 and 3141, and the catalog has courses 1045, 3141 and 4022
  When  The instructor is saved with courses 3141 and 4022 selected
  Then  An assignment for 4022 is added, the assignment for 1045 is deleted, 3141 stays unchanged, and the instructor now teaches 3141 and 4022
**Parameters:** Comparison is done on the course ID as a string against every course in the catalog (db.Courses).
**Edge cases handled:** selectedCourses null (no boxes ticked): CourseAssignments is replaced with an empty list, so every existing assignment is dropped; Selected IDs that are not in the course catalog are ignored; On Create (lines 72-80) each selected ID is parsed with int.Parse and added with no catalog check; a non-numeric value throws an exception
**Suspected defect:** When nothing is selected, the code replaces the collection instead of marking each assignment Deleted, so whether old rows are actually deleted or left orphaned depends on how EF Core handles the relationship. On Create, CourseAssignment.InstructorID is set from instructor.ID before the save, while it is still 0; this only works because EF fixes up the navigation.
**Confidence:** High

### RULE-028: Deleting an instructor unassigns them as department administrator
**Category:** Lifecycle
**Priority:** P1
**Source:** `Controllers/InstructorsController.cs:227-250`
**Plain English:** When an instructor is deleted, any department they administer is left with no administrator, so the department is kept and is not left pointing at a deleted person.
**Specification:**
  Given Instructor 5 administers the English department and has office 'Gowan 27'
  When  An instructor deletion is confirmed for ID 5
  Then  The instructor and their office assignment are removed, English.InstructorID is set to null, the change is saved, and a DELETE notification is sent for Instructor 5
**Parameters:** The department lookup uses SingleOrDefault on Departments where InstructorID equals the deleted ID.
**Edge cases handled:** The instructor administers no department: only the instructor is removed; The instructor administers 2 or more departments: SingleOrDefault throws and the delete fails; The instructor ID does not exist: Single() throws (unhandled); Course assignments are not removed explicitly, so this relies on a database or EF cascade
**Suspected defect:** An instructor who administers more than one department cannot be deleted, because SingleOrDefault throws an InvalidOperationException instead of clearing every matching department.
**Confidence:** Medium — P0 panel split on whether this is critical to the system's core purpose or a costly-if-wrong rule (Faithful: I checked legacy/contoso/Controllers/InstructorsController.cs:227-250. DeleteConfirmed loads the instructor together with their office assignment (.Single() at line 232) and removes the instructor. It then finds the one department whose InstructorID matches (SingleOrDefault at 236-238) and…

### RULE-029: Student record lifecycle with change notifications
**Category:** Lifecycle
**Priority:** P1
**Source:** `Controllers/StudentsController.cs:109-119`
**Plain English:** A student is created, updated or deleted only after validation passes and the database save succeeds, and each successful change emits a CREATE/UPDATE/DELETE notification naming the student.
**Specification:**
  Given A valid new student 'Carson Alexander' enrolled 2010-09-01
  When  The record is saved
  Then  The student is persisted, a 'Student' CREATE notification with the new ID and display name 'Carson Alexander' is sent by user 'System', and the user is redirected to the student list
**Parameters:** Entity type 'Student'; operations EntityOperation.CREATE (line 116), UPDATE (line 170), DELETE (line 211); notifying user hardcoded 'System' (BaseController.cs:28); display name format '{FirstMidName} {LastName}'
**Edge cases handled:** Notification is sent only after SaveChanges succeeds; notification failures are swallowed and do not roll back the change (BaseController.cs:26-35); Delete captures the display name before removal so the DELETE notification still names the student (lines 205-211); Delete failure (e.g. student not found, or DB constraint because of existing enrollments) redirects to the list with TempData error 'Unable to delete the student...' (lines 215-219); Save failure on Create/Edit redisplays the form with 'Unable to save changes. Try again...'; Hard delete - no soft-delete/inactive status for students
**Suspected defect:** DeleteConfirmed (line 205-206) does not null-check Find(id); a missing student raises an exception that is reported as a generic delete failure rather than 'not found'.
**Confidence:** Medium — When a student who has enrollments is deleted, should the enrollments be cascade-deleted, should the delete be blocked, or should the student be deactivated instead? The code relies on the database's default FK behavior and has no explicit rule.

### RULE-030: One-time reference data seeding gated on existence of any student
**Category:** Lifecycle
**Priority:** P1
**Source:** `Data/DbInitializer.cs:9-18`
**Also cited:** Global.asax.cs:14-35
**Plain English:** At startup the database is created if missing, and sample school data is loaded only when there are no students yet; if even one student exists, seeding is skipped entirely.
**Specification:**
  Given A database that already contains 1 student record (and no departments, courses, or instructors)
  When  DbInitializer.Initialize runs at application start
  Then  No seed data is inserted at all (instructors, departments, courses, office assignments, course assignments, and enrollments are all skipped) because the gate checks only the Students set
**Parameters:** Gate condition: context.Students.Any() == false; schema creation via EnsureCreated (not migrations)
**Edge cases handled:** Empty database: EnsureCreated builds schema, then the full set is inserted in order Students -> Instructors -> Departments -> Courses -> OfficeAssignments -> CourseAssignments -> Enrollments, saving…; Partially seeded DB (students present, other tables empty) is never completed; EnsureCreated does not apply schema changes to an existing database
**Suspected defect:** The gate checks only Students; if a previous seed failed after the students were saved, the remaining reference data is never loaded. Because saves happen per entity group with no wrapping transaction, partial seeding is possible.
**Confidence:** High

### RULE-031: Notification creation on entity change (fire-and-forget)
**Category:** Lifecycle
**Priority:** P1
**Source:** `Services/NotificationService.cs:39-68`
**Plain English:** Each create, update or delete of an entity publishes an unread notification to a message queue. It records who made the change (or 'System' when nobody is known) and the time, and a failed send never blocks the change itself.
**Specification:**
  Given A Student with ID 42 is updated by user 'jdoe'
  When  SendNotification('Student','42',null,UPDATE,'jdoe') is called
  Then  A message labelled 'Student UPDATE' with Normal priority is queued, containing Operation='UPDATE', CreatedBy='jdoe', IsRead=false, CreatedAt=server local time. If the queue send throws, the error is only written to debug output and the entity change still succeeds.
**Parameters:** Default CreatedBy='System'; message priority=Normal; queue path from AppSetting NotificationQueuePath, default .\Private$\ContosoUniversityNotifications; CreatedAt uses DateTime.Now (local time, not UTC)
**Edge cases handled:** userName null -> CreatedBy='System'; Queue failure is swallowed, so the notification is silently lost; Queue is auto-created if missing and given FullControl for 'Everyone' (lines 20-24); Model length limits (EntityType 100, EntityId 50, Operation 20, Message 256, CreatedBy 100) are not enforced on the queue path
**Suspected defect:** Auto-created queue grants 'Everyone' FullControl, so anyone can read, inject or purge notifications. Notifications are lost without any trace when sending fails. Times are recorded in server local time, not UTC.
**Confidence:** High

### RULE-032: Mark-as-read is a no-op (IsRead/ReadAt lifecycle not implemented)
**Category:** Lifecycle
**Priority:** P1
**Source:** `Services/NotificationService.cs:90-94`
**Plain English:** Notifications have an Unread/Read status with a read timestamp, but marking one as read does nothing and still reports success.
**Specification:**
  Given A notification with Id 7
  When  POST /Notifications/MarkAsRead?id=7
  Then  The controller returns success=true, but IsRead stays false and ReadAt is never set. Nothing is saved.
**Parameters:** Model fields IsRead (bool, set to false on creation) and ReadAt (datetime2, nullable) in Models/Notification.cs:35-38; controller action at Controllers/NotificationsController.cs:45-57
**Edge cases handled:** Notification Id is never assigned on the queue path (always 0), so the id cannot identify a notification
**Suspected defect:** The read-status lifecycle is declared but not implemented, and the endpoint reports success anyway.
**Confidence:** High

## Policy

### RULE-033: No authentication or authorization required for any page
**Category:** Policy
**Priority:** P0
**Source:** `App_Start/FilterConfig.cs:7-12`
**Plain English:** Anyone who can reach the site can view and change all records; the only global filter is the error handler, and the global login requirement is commented out.
**Specification:**
  Given An anonymous visitor with no login
  When  They request any controller action (including create, edit, delete)
  Then  The request is served; only HandleErrorAttribute is applied globally, no AuthorizeAttribute exists anywhere in the codebase
**Parameters:** Global filters: HandleErrorAttribute only; AuthorizeAttribute commented out at line 11
**Edge cases handled:** The comment at line 10 claims role-based authorization is implemented instead, but no [Authorize] attribute exists anywhere in the .cs sources
**Suspected defect:** Comment says global authorization was removed 'since we're implementing role-based authorization', but no role-based authorization exists in code; every write operation is publicly accessible.
**Confidence:** High

### RULE-034: Change notifications are attributed to 'System' and are best-effort
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/BaseController.cs:19-36`
**Plain English:** Whenever a screen creates, updates or deletes a record it sends a change notification naming the entity, its id and optional display name, always credited to the user 'System', and a notification failure never blocks the data change.
**Specification:**
  Given A user edits Student id 42 with display name 'Alexander Carson'
  When  The controller calls SendEntityNotification("Student","42","Alexander Carson",Update)
  Then  A notification is sent to the notification queue with user name 'System'; if sending throws, the error is only written to debug output and the edit still succeeds
**Parameters:** Default user name: "System" (hardcoded, line 28); queue path: .\Private$\ContosoUniversityNotifications (Web.config:19); display name optional (null when omitted, line 21)
**Edge cases handled:** Notification failure is swallowed silently: no retry, no audit of the failure; Actual user identity is never captured, so audit trail cannot identify who made a change
**Suspected defect:** Audit/notification trail is effectively anonymous ('System' for every change) and lost notifications are not recorded anywhere persistent.
**Confidence:** High

### RULE-035: Teaching material image storage and naming
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/CoursesController.cs:73-95`
**Plain English:** Accepted images are stored in the Uploads/TeachingMaterials folder under a unique name built from the course number and a random GUID, and the course record stores that virtual path; if saving fails the course is not saved.
**Specification:**
  Given Course number 1050 with an accepted file "Diagram.JPG"
  When  The course is created (or edited, CoursesController.cs:156-188)
  Then  The file is saved as ~/Uploads/TeachingMaterials/course_1050_<guid>.jpg and TeachingMaterialImagePath is set to that value; on any I/O exception the form is redisplayed with "Error uploading file: <message>" and no database change is made.
**Parameters:** Storage folder ~/Uploads/TeachingMaterials/ (created if missing); file name pattern course_{CourseID}_{GUID}{lower-cased extension}
**Edge cases handled:** Original file name is discarded except for the extension; If the DB save fails after the file was written, the orphaned file remains on disk
**Confidence:** High

### RULE-036: Blank office location removes the instructor's office assignment
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/InstructorsController.cs:149-157`
**Plain English:** If an instructor is saved with an empty or whitespace-only office location, their office assignment is removed rather than stored as blank.
**Specification:**
  Given Instructor 9 has office 'Smith 17'
  When  The instructor is edited and the office location is set to '   '
  Then  The office assignment is set to null (removed) and the other fields save normally
**Parameters:** Only the fields LastName, FirstMidName, HireDate and OfficeAssignment can be updated. The office location can be at most 50 characters (OfficeAssignment model).
**Edge cases handled:** The location check runs only on Edit. On Create, a blank OfficeAssignment is bound as-is; If OfficeAssignment is null after binding, reading .Location throws; the catch turns this into the generic 'Unable to save changes' error
**Suspected defect:** A possible null dereference on instructorToUpdate.OfficeAssignment.Location when the instructor has no office and none is posted. The resulting error is hidden behind a generic save-failure message.
**Confidence:** High

### RULE-037: Delete authorization stated in comments is not enforced
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/InstructorsController.cs:224-227`
**Plain English:** The code comments say only admins may delete instructors and that all roles can view, but no executable authorization exists, so any user can delete instructors and departments.
**Specification:**
  Given An anonymous user with no admin role
  When  They POST to Instructors/Delete/5
  Then  The instructor is deleted. No role check runs (there is no [Authorize] attribute, and the global AuthorizeAttribute is commented out in App_Start/FilterConfig.cs:11)
**Parameters:** Role intent appears in comments only: 'Only admins can delete instructors' (line 224) and 'All roles can view' (lines 15, 43; DepartmentsController.cs:13).
**Suspected defect:** The comments claim an admin-only delete, but the code does not enforce it; anyone can delete.
**Confidence:** Low — Is deleting instructors (and departments) meant to be limited to administrators, and which roles may create or edit them? The code enforces no authorization.

### RULE-038: Notification retrieval is destructive and capped at 10 per poll
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/NotificationsController.cs:13-41`
**Plain English:** Each request for notifications takes up to 10 messages off the shared queue and removes them, so whichever browser polls first gets them and no other admin ever sees them.
**Specification:**
  Given 15 notifications are waiting in the queue
  When  An admin's browser calls GET /Notifications/GetNotifications
  Then  The first 10 are removed from the queue and returned with success=true and count=10. The remaining 5 come back on the next poll. Each receive waits up to 1 second, and an empty queue ends the batch.
**Parameters:** Batch cap=10; receive timeout=1 second per message
**Edge cases handled:** Empty queue -> success=true, count=0; Any error -> success=false with the message 'Error retrieving notifications'; A message that cannot be deserialized returns null and ends the batch early (it has already been removed from the queue)
**Suspected defect:** There is no authorization check on GetNotifications, even though comments say it is for admins. Because receives are destructive, notifications go to whichever client polls first, and a message that fails to deserialize is lost.
**Confidence:** Medium — Should every admin user see every notification? Right now the queue read is destructive and shared, so each notification reaches only one browser session. Is the endpoint meant to be limited to admins? No authorization attribute is present.

### RULE-039: Student screens intended for Admins and Teachers but not enforced
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/StudentsController.cs:14-15`
**Plain English:** Comments state only Admins and Teachers may view students, but no authorization check exists, so anyone can view, create, edit and delete students.
**Specification:**
  Given An anonymous user with no role
  When  They open Students/Index, Details, or post Create/Edit/Delete
  Then  The request is served; all actions are recorded under user 'System'
**Parameters:** Intended roles (comment only): Admins, Teachers (lines 14, 62); no [Authorize] attribute in the controller; BaseController.cs:28 notes 'No authentication'
**Edge cases handled:** Anti-forgery tokens are required on POST Create/Edit/Delete (lines 92, 146, 200) - the only request guard
**Suspected defect:** Authorization stated in comments is not implemented; student PII is open to unauthenticated users, and the audit trail cannot identify who made a change.
**Confidence:** Low — Which roles should be allowed to view versus create/edit/delete student records in the new system, and is the 'Admins and Teachers can view' comment the intended policy?

### RULE-040: Only name and enrollment date may be set from the student form
**Category:** Policy
**Priority:** P1
**Source:** `Controllers/StudentsController.cs:93`
**Plain English:** The student create/edit forms accept only last name, first/middle name and enrollment date (plus ID on edit); enrollments and grades cannot be changed through the student screen.
**Specification:**
  Given A POST to Students/Create containing LastName, FirstMidName, EnrollmentDate and an extra Enrollments payload
  When  The request is model-bound
  Then  Only LastName, FirstMidName and EnrollmentDate are bound; enrollments are ignored
**Parameters:** Create allowlist: LastName, FirstMidName, EnrollmentDate (line 93); Edit allowlist: ID, LastName, FirstMidName, EnrollmentDate (line 147)
**Edge cases handled:** Edit marks the whole entity Modified (line 165), so all bound fields are overwritten; no optimistic concurrency check - last writer wins; Edit with an ID that no longer exists throws on save and shows the generic 'Unable to save changes' message
**Confidence:** High

### RULE-041: Person stored as a single table, with Student/Instructor role set by a discriminator
**Category:** Policy
**Priority:** P1
**Source:** `Data/SchoolContext.cs:47-53`
**Plain English:** Students and instructors are both people stored in one Person table, and a Discriminator column tells which kind each person is.
**Specification:**
  Given A new Student 'Carson Alexander' and a new Instructor 'Kim Abercrombie'
  When  Both are saved
  Then  Both rows go into the Person table, with Discriminator = 'Student' and 'Instructor' respectively
**Parameters:** Table: Person; Discriminator column: 'Discriminator' (string); values 'Student', 'Instructor'
**Edge cases handled:** A person cannot be both a student and an instructor under one record; Student-specific (EnrollmentDate) and instructor-specific (HireDate) columns share the table and are null for the other type
**Confidence:** High

### RULE-042: Course numbers are business-assigned, not auto-generated
**Category:** Policy
**Priority:** P1
**Source:** `Models/Course.cs:9-11`
**Also cited:** (with seed examples at Data/DbInitializer.cs:88-111)
**Plain English:** Courses are identified by catalog numbers chosen by the institution (e.g., 1050 Chemistry), and each course belongs to one department and carries a fixed credit value.
**Specification:**
  Given A new course with CourseID 1050, Title 'Chemistry', Credits 3, Department Engineering
  When  It is saved
  Then  It is stored with key 1050 exactly as supplied (no identity generation)
**Parameters:** Course.CourseID DatabaseGenerated(None) (Models/Course.cs:9); seed catalog: 1050 Chemistry 3cr Engineering, 4022 Microeconomics 3cr Economics, 4041 Macroeconomics 3cr Economics, 1045 Calculus 4cr Mathematics, 3141 Trigonometry 4cr Mathematics, 2021 Composition 3cr English, 2042 Literature 4cr English
**Edge cases handled:** Duplicate course numbers are rejected as a primary-key violation
**Suspected defect:** Chemistry is seeded under the Engineering department, which looks like a data error in the sample data.
**Confidence:** Medium — Citation was corrected by referee (The cited lines, legacy/contoso/Data/DbInitializer.cs:88-111, are seed data. They build seven Course objects with explicit CourseIDs, titles, credits and departments: 1050 Chemistry 3cr Engineering, 4022 Microeconomics 3cr Economics, 4041 Macroeconomics 3cr Economics, 1045 Calculus 4cr Mathematics, 3141 Trigonometry 4cr Mathematics, 2021 Composition 3cr English,…

### RULE-043: Department administrator is optional and must be an instructor
**Category:** Policy
**Priority:** P1
**Source:** `Models/Department.cs:24-29`
**Plain English:** Each department may have at most one administrator, who must be an instructor; a department can also have no administrator.
**Specification:**
  Given Department 'Mathematics' with InstructorID null
  When  The department is saved
  Then  It is accepted with no administrator; if InstructorID = 3 it links to instructor #3 as Administrator
**Parameters:** InstructorID nullable int FK to Instructor (Administrator)
**Edge cases handled:** Same instructor may administer multiple departments (no uniqueness constraint); No check that the administrator teaches in that department
**Confidence:** Medium — Is an instructor allowed to administer more than one department, and must a department always have an administrator?

### RULE-044: Default landing page and URL scheme
**Category:** Policy
**Priority:** P2
**Source:** `App_Start/RouteConfig.cs:8-17`
**Plain English:** Pages are addressed as /Area/Action/Id, and visiting the site root shows the Home page.
**Specification:**
  Given A user browses to the site root '/'
  When  The URL is routed
  Then  Home/Index is displayed; '/Students/Edit/5' maps to the Students controller, Edit action, record id 5; id is optional
**Parameters:** Default controller=Home, action=Index, id optional
**Edge cases handled:** *.axd resource requests are excluded from routing
**Confidence:** High

### RULE-045: Change notifications on instructor and department create/update/delete
**Category:** Policy
**Priority:** P2
**Source:** `Controllers/DepartmentsController.cs:151-165`
**Plain English:** Every successful create, update or delete of an instructor or department sends a change notification with the entity type, ID, display name (departments only) and user 'System'. A failed notification never blocks the change.
**Specification:**
  Given The Physics department (ID 4) exists
  When  Its deletion is confirmed
  Then  The department is removed, and then a DELETE notification is sent for Department 4 with display name 'Physics' and user 'System'
**Parameters:** The user name is hardcoded as 'System' (BaseController.cs:28). Instructor notifications have no display name (InstructorsController.cs:87,164,247). Department notifications are at DepartmentsController.cs:53, 91 and 162.
**Edge cases handled:** Notification send fails: the exception is swallowed and only written to the debug output; Department delete confirmed for an ID that does not exist: department.Name throws a null reference before anything is removed; The department delete does not check RowVersion and does not block deletion when courses are linked
**Suspected defect:** The actor is always 'System', so there is no real audit trail of who made a change. Deleting a department does not check whether courses still reference it.
**Confidence:** High

### RULE-046: Instructor directory drill-down (instructor to courses to enrollments)
**Category:** Policy
**Priority:** P2
**Source:** `Controllers/InstructorsController.cs:16-41`
**Plain English:** The instructor list is sorted by last name. Selecting an instructor shows the courses they teach, and then selecting one of those courses shows its enrollments.
**Specification:**
  Given Instructors Abercrombie, Fakhouri and Zheng, where Fakhouri (ID 2) teaches course 4022
  When  Index is requested with id=2 and courseID=4022
  Then  Instructors are listed in last-name order, Fakhouri's courses are shown, and the enrollments for course 4022 are shown
**Parameters:** Sort key: LastName ascending.
**Edge cases handled:** courseID given without id: Courses is null, so a null reference error occurs; A courseID not taught by the selected instructor: Single() throws
**Confidence:** High

### RULE-047: Student list search, sort and paging
**Category:** Policy
**Priority:** P2
**Source:** `Controllers/StudentsController.cs:15-59`
**Plain English:** The student list can be filtered by a text fragment matching last name or first name, sorted by last name (default ascending) or enrollment date, and is shown 10 per page, returning to page 1 whenever a new search is entered.
**Specification:**
  Given 25 students, 3 of whom have 'an' in their first or last name
  When  A user searches 'an' while on page 3
  Then  Paging resets to page 1 and only the 3 matching students are shown, ordered by last name ascending
**Parameters:** Page size 10 (line 57); default page 1; sort keys: default = LastName asc, 'name_desc' = LastName desc, 'Date' = EnrollmentDate asc, 'date_desc' = EnrollmentDate desc
**Edge cases handled:** Empty search string shows all students; Search is a substring 'contains' match; case sensitivity depends on database collation; Sorting by name uses LastName only (no tie-break on first name); Paging state preserved via currentFilter when navigating pages
**Confidence:** High

### RULE-048: New student defaults to today's enrollment date
**Category:** Policy
**Priority:** P2
**Source:** `Controllers/StudentsController.cs:81-88`
**Plain English:** When opening the new-student form, the enrollment date is pre-filled with today's date.
**Specification:**
  Given Today is 2026-10-26
  When  A user opens the Create Student page
  Then  The Enrollment Date field is pre-populated with 2026-10-26 and can be overridden
**Parameters:** Default = DateTime.Today (server local date, no time component)
**Edge cases handled:** Server time zone determines 'today'
**Confidence:** High

### RULE-049: Department has budget, start date and optional administrator instructor
**Category:** Policy
**Priority:** P2
**Source:** `Data/DbInitializer.cs:66-86`
**Plain English:** Each department records a budget, a start date and optionally one instructor who acts as its administrator.
**Specification:**
  Given Department English with Budget 350,000, StartDate 2007-09-01, administrator Abercrombie
  When  The seed runs
  Then  The department is stored with InstructorID pointing to Abercrombie
**Parameters:** Seed: English 350000 (Abercrombie), Mathematics 100000 (Fakhouri), Engineering 350000 (Harui), Economics 100000 (Kapoor); all StartDate 2007-09-01; Department.InstructorID is nullable (Models/Department.cs:24)
**Edge cases handled:** Administrator is optional (nullable FK)
**Confidence:** Medium — Is the Department.InstructorID 'administrator' role a real business role, and are there rules such as the administrator having to belong to the department or a limit on how many departments one instructor can administer? None are enforced in this code.

## Rules requiring SME confirmation

- **RULE-006** (Medium): P0 panel doubts spec fidelity: Most of the card matches the code. Department.RowVersion has a [Timestamp] attribute (Models/Department.cs:26-27), so EF throws DbUpdateConcurrencyException when a save uses a stale token. Controllers/DepartmentsController.cs:96-128 handles it this way. If the row was deleted, it shows the 'deleted by another user' message. Otherwise it compares Name, Budget, StartD…
- **RULE-007** (Medium): P0 panel split on whether this is critical to the system's core purpose or a costly-if-wrong rule (The rule card matches the code. In legacy/contoso/Controllers/CoursesController.cs, lines 52-71 (Create) and 135-154 (Edit) only check a file when one is attached and is not empty (ContentLength > 0). The extension is lower-cased with ToLower, so the check ignores case, and it must be one of .jpg, .…
- **RULE-008** (Medium): Should the department budget have a minimum (for example >= 0) or a maximum, and should the department name be required? Neither is enforced today.
- **RULE-010** (Medium): P0 panel split on whether this is critical to the system's core purpose or a costly-if-wrong rule (The rule card matches the code, but this rule should not be P0. Faithful: StudentsController.cs:97-107 (Create) adds the error "Please enter a valid enrollment date." when EnrollmentDate is DateTime.MinValue or default. It adds "Enrollment date must be between 1753 and 9999." when the date is before…
- **RULE-011** (Medium): Is 'a student can enroll in a course only once' a real business rule? If so, should it be a database unique constraint (it currently exists only in the seeder), and what about students retaking a course?
- **RULE-012** (Medium): Citation was corrected by referee (Models/CourseAssignment.cs:8-14 is only a plain join-entity POCO: InstructorID, CourseID and two navigation properties. It has no [Key] attribute, no index and no logic, so it does not enforce uniqueness itself. The rule is real but lives elsewhere. Data/SchoolContext.cs:55-57 sets the composite primary key HasKey(c => new { c.CourseID, c.InstructorID }), which…
- **RULE-014** (Medium): Should a department name be mandatory, and should Budget be constrained to non-negative values? The current model allows a blank name and any budget amount.
- **RULE-019** (Medium): Citation was corrected by referee (The behavior is real, but most of it is not in the cited lines. Models/Student.cs:8-16 only shows that Student inherits from Person (line 8) and puts [Required] on EnrollmentDate (line 10), plus a Range limit of 1753-9999 (line 15) that the rule leaves out. The name checks the rule is mainly about live in Models/Person.cs. LastName is [Required] with [StringLeng…
- **RULE-020** (Medium): Is 10 MB the business-mandated maximum file upload size (e.g., for instructor photos/documents), and is the 1-hour execution timeout intentional?
- **RULE-025** (Medium): Should a course with enrollments or instructor assignments be deletable, and if so should its enrollments be removed (cascade) or should the deletion be blocked?
- **RULE-028** (Medium): P0 panel split on whether this is critical to the system's core purpose or a costly-if-wrong rule (Faithful: I checked legacy/contoso/Controllers/InstructorsController.cs:227-250. DeleteConfirmed loads the instructor together with their office assignment (.Single() at line 232) and removes the instructor. It then finds the one department whose InstructorID matches (SingleOrDefault at 236-238) and…
- **RULE-029** (Medium): When a student who has enrollments is deleted, should the enrollments be cascade-deleted, should the delete be blocked, or should the student be deactivated instead? The code relies on the database's default FK behavior and has no explicit rule.
- **RULE-037** (Low): Is deleting instructors (and departments) meant to be limited to administrators, and which roles may create or edit them? The code enforces no authorization.
- **RULE-038** (Medium): Should every admin user see every notification? Right now the queue read is destructive and shared, so each notification reaches only one browser session. Is the endpoint meant to be limited to admins? No authorization attribute is present.
- **RULE-039** (Low): Which roles should be allowed to view versus create/edit/delete student records in the new system, and is the 'Admins and Teachers can view' comment the intended policy?
- **RULE-042** (Medium): Citation was corrected by referee (The cited lines, legacy/contoso/Data/DbInitializer.cs:88-111, are seed data. They build seven Course objects with explicit CourseIDs, titles, credits and departments: 1050 Chemistry 3cr Engineering, 4022 Microeconomics 3cr Economics, 4041 Macroeconomics 3cr Economics, 1045 Calculus 4cr Mathematics, 3141 Trigonometry 4cr Mathematics, 2021 Composition 3cr English,…
- **RULE-043** (Medium): Is an instructor allowed to administer more than one department, and must a department always have an administrator?
- **RULE-049** (Medium): Is the Department.InstructorID 'administrator' role a real business role, and are there rules such as the administrator having to belong to the department or a limit on how many departments one instructor can administer? None are enforced in this code.

## Rules folded into another

These rules described the same behavior as another rule in a different place, so they were merged into it (the kept rule lists their locations under "Also cited"):

- Database is created and seeded once at application startup (Global.asax.cs:14-35) into One-time reference data seeding gated on existence of any student
- Department edits use optimistic concurrency (row version) (Models/Department.cs:26-27) into Department edits use optimistic concurrency (first save wins)
- Instructor-course teaching assignment is unique per pair (Data/SchoolContext.cs:55-57 (composite key); Controllers/InstructorsController.cs:177-207 (add/remo…) into Instructor can be assigned to a given course at most once (many-to-many teaching assignment)
- Instructor has at most one office assignment (Data/SchoolContext.cs:70-74) into Instructor has at most one office; office location max 50 chars
- Enrollment grade is optional (ungraded enrollments allowed) (Data/DbInitializer.cs:212-215) into Enrollment grade scale A-F, optional
