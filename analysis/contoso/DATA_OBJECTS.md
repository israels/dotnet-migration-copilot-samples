# Data Objects — contoso

## Person (abstract, TPH base)
Source: `legacy/contoso/Models/Person.cs:6`

| Field | Type | Note |
|---|---|---|
| ID | int | PK, identity by convention (Person.cs:8) |
| LastName | string | [Required], [StringLength(50)], display 'Last Name' (Person.cs:10-13) |
| FirstMidName | string | [Required], [StringLength(50)], mapped to column 'FirstName' (Person.cs:15-19) |
| FullName | string (computed, read-only) | LastName + ", " + FirstMidName; not persisted (Person.cs:21-28) |
| Discriminator | string (shadow column) | Values 'Student' / 'Instructor'; single table 'Person' (Data/SchoolContext.cs:49-53) |

Used by: Person stored as a single table, with Student/Instructor role set by a discrimi…, Person name is required and limited to 50 characters, Full name display format, Student identity fields are required and length-limited, Only name and enrollment date may be set from the student form, Student list search, sort and paging

## Student
Source: `legacy/contoso/Models/Student.cs:8`

| Field | Type | Note |
|---|---|---|
| (inherits Person) | Person | ID, LastName, FirstMidName, FullName |
| EnrollmentDate | DateTime | [Required], datetime2, [Range 1/1/1753-12/31/9999], format yyyy-MM-dd (Student.cs:10-16) |
| Enrollments | ICollection<Enrollment> | navigation (Student.cs:18) |

Used by: Person stored as a single table, with Student/Instructor role set by a discrimi…, Student enrollment date must be a real date within the 1753-9999 range, Student identity fields are required and length-limited, New student defaults to today's enrollment date, Only name and enrollment date may be set from the student form, Student record lifecycle with change notifications, Student list search, sort and paging, Student screens intended for Admins and Teachers but not enforced, Missing student id handling on detail/edit/delete views, One-time reference data seeding gated on existence of any student, Student enrollment statistics by enrollment date, Instructor directory drill-down (instructor to courses to enrollments)

## Instructor
Source: `legacy/contoso/Models/Instructor.cs:8`

| Field | Type | Note |
|---|---|---|
| (inherits Person) | Person | ID, LastName, FirstMidName, FullName |
| HireDate | DateTime | [Required], datetime2, [Range 1/1/1753-12/31/9999] (Instructor.cs:10-16) |
| CourseAssignments | ICollection<CourseAssignment> | many-to-many to Course via join entity (Instructor.cs:18) |
| OfficeAssignment | OfficeAssignment | optional 1:1 (Instructor.cs:19; SchoolContext.cs:71-74) |

Used by: Person stored as a single table, with Student/Instructor role set by a discrimi…, Instructor create requires a valid hire date, Instructor hire date is required and must fall within 1753-9999, Instructor course assignments are synchronized to the selected course set, Blank office location removes the instructor's office assignment, Deleting an instructor unassigns them as department administrator, Instructor has at most one office; office location max 50 chars, Instructor can be assigned to a given course at most once (many-to-many teachin…, Instructor directory drill-down (instructor to courses to enrollments), Change notifications on instructor and department create/update/delete, Delete authorization stated in comments is not enforced, Department administrator is optional and must be an instructor

## Course
Source: `legacy/contoso/Models/Course.cs:7`

| Field | Type | Note |
|---|---|---|
| CourseID | int | PK, [DatabaseGenerated(None)] - business-assigned; display 'Number' (Course.cs:9-11) |
| Title | string | [StringLength(50, MinimumLength=3)], not [Required] (Course.cs:13-14) |
| Credits | int | [Range(0,5)] (Course.cs:16-17) |
| DepartmentID | int | FK to Department, non-nullable (Course.cs:19) |
| TeachingMaterialImagePath | string | [StringLength(255)], relative path of uploaded image (Course.cs:21-23) |
| Department | Department | navigation (Course.cs:25) |
| Enrollments | ICollection<Enrollment> | navigation (Course.cs:26) |
| CourseAssignments | ICollection<CourseAssignment> | navigation (Course.cs:27) |

Used by: Course numbers are business-assigned, not auto-generated, Course record field constraints, Teaching material image upload acceptance (type and size), Teaching material image storage and naming, Image replacement on course edit removes previous file, Course deletion removes its image and the course, Course change notifications, Course lookup requires an id and an existing course, Instructor course assignments are synchronized to the selected course set, Instructor directory drill-down (instructor to courses to enrollments), Maximum request/upload size of 10 MB, Duplicate enrollment prevention (one enrollment per student per course) during…

## Enrollment (+ enum Grade)
Source: `legacy/contoso/Models/Enrollment.cs:10`

| Field | Type | Note |
|---|---|---|
| EnrollmentID | int | PK (Enrollment.cs:12) |
| CourseID | int | FK to Course (Enrollment.cs:13) |
| StudentID | int | FK to Person/Student (Enrollment.cs:14) |
| Grade | Grade? (enum A,B,C,D,F) | nullable; NullDisplayText 'No grade' (Enrollment.cs:5-8,15-16) |
| Course | Course | navigation |
| Student | Student | navigation |

Used by: Enrollment grade scale A-F, optional, Duplicate enrollment prevention (one enrollment per student per course) during…, Instructor directory drill-down (instructor to courses to enrollments), One-time reference data seeding gated on existence of any student

## Department
Source: `legacy/contoso/Models/Department.cs:8`

| Field | Type | Note |
|---|---|---|
| DepartmentID | int | PK, identity (Department.cs:10) |
| Name | string | [StringLength(50, MinimumLength=3)], not [Required] (Department.cs:12-13) |
| Budget | decimal | SQL 'money', currency display (Department.cs:15-17) |
| StartDate | DateTime | datetime2 via convention, format yyyy-MM-dd (Department.cs:19-22; SchoolContext.cs:27-38) |
| InstructorID | int? | optional FK to administrator Instructor (Department.cs:24) |
| RowVersion | byte[] | [Timestamp] concurrency token (Department.cs:26-27) |
| Administrator | Instructor | navigation (Department.cs:29) |
| Courses | ICollection<Course> | navigation (Department.cs:30) |

Used by: Department has budget, start date and optional administrator instructor, Department edits use optimistic concurrency (first save wins), Department create/edit field rules, Department name length 3-50 characters (but not required), Department administrator is optional and must be an instructor, Deleting an instructor unassigns them as department administrator, Change notifications on instructor and department create/update/delete, Delete authorization stated in comments is not enforced

## CourseAssignment (join entity)
Source: `legacy/contoso/Models/CourseAssignment.cs:8`

| Field | Type | Note |
|---|---|---|
| InstructorID | int | composite PK part, FK to Instructor (CourseAssignment.cs:10; SchoolContext.cs:56-68) |
| CourseID | int | composite PK part, FK to Course (CourseAssignment.cs:11) |
| Instructor | Instructor | navigation |
| Course | Course | navigation |

Used by: Instructor can be assigned to a given course at most once (many-to-many teachin…, Instructor course assignments are synchronized to the selected course set, Instructor directory drill-down (instructor to courses to enrollments)

## OfficeAssignment
Source: `legacy/contoso/Models/OfficeAssignment.cs:6`

| Field | Type | Note |
|---|---|---|
| InstructorID | int | [Key] and FK to Instructor (shared-PK 1:1) (OfficeAssignment.cs:8-9; SchoolContext.cs:71-74) |
| Location | string | [StringLength(50)], display 'Office Location' (OfficeAssignment.cs:10-12) |
| Instructor | Instructor | navigation |

Used by: Instructor has at most one office; office location max 50 chars, Blank office location removes the instructor's office assignment, Instructor directory drill-down (instructor to courses to enrollments)

## Notification (+ enum EntityOperation)
Source: `legacy/contoso/Models/Notification.cs:7`

| Field | Type | Note |
|---|---|---|
| Id | int | [Key]; never assigned by NotificationService (Services/NotificationService.cs:43-52), so it is always 0 in queued messages |
| EntityType | string | [Required], [StringLength(100)] |
| EntityId | string | [Required], [StringLength(50)] |
| Operation | string | [Required], [StringLength(20)]; set from EntityOperation enum CREATE/UPDATE/DELETE (Notification.cs:22,41-46) |
| Message | string | [Required], [StringLength(256)]; built by GenerateMessage (NotificationService.cs:96-113) |
| CreatedAt | DateTime | [Required], datetime2; DateTime.Now at send |
| CreatedBy | string | [StringLength(100)]; defaults to 'System' (NotificationService.cs:50) |
| IsRead | bool | always false at creation; never updated (MarkAsRead is empty, NotificationService.cs:90-94) |
| ReadAt | DateTime? | datetime2; never set |

Used by: Notification creation on entity change (fire-and-forget), Notification message wording, Notification retrieval is destructive and capped at 10 per poll, Mark-as-read is a no-op (IsRead/ReadAt lifecycle not implemented), Relative time display ('time ago'), Change notifications are attributed to 'System' and are best-effort, Student record lifecycle with change notifications, Course change notifications, Change notifications on instructor and department create/update/delete

## PaginatedList<T>
Source: `legacy/contoso/PaginatedList.cs:7`

| Field | Type | Note |
|---|---|---|
| (items) | List<T> | inherits List<T>; Skip((pageIndex-1)*pageSize).Take(pageSize) (PaginatedList.cs:27) |
| PageIndex | int | 1-based (PaginatedList.cs:9) |
| TotalPages | int | ceil(count/pageSize) (PaginatedList.cs:15) |
| HasPreviousPage | bool (computed) | PageIndex > 1 |
| HasNextPage | bool (computed) | PageIndex < TotalPages |

Used by: Paged result window and page count, Student list search, sort and paging

## EnrollmentDateGroup (view model)
Source: `legacy/contoso/Models/SchoolViewModels/EnrollmentDateGroup.cs:6`

| Field | Type | Note |
|---|---|---|
| EnrollmentDate | DateTime? | [DataType(Date)] group key |
| StudentCount | int | count of students per date; produced in Controllers/HomeController.cs:18-21 |

Used by: Student enrollment statistics by enrollment date

## InstructorIndexData (view model)
Source: `legacy/contoso/Models/SchoolViewModels/InstructorIndexData.cs:5`

| Field | Type | Note |
|---|---|---|
| Instructors | IEnumerable<Instructor> |  |
| Courses | IEnumerable<Course> | courses of selected instructor |
| Enrollments | IEnumerable<Enrollment> | enrollments of selected course; built in Controllers/InstructorsController.cs:18 |

Used by: Instructor directory drill-down (instructor to courses to enrollments)

## AssignedCourseData (view model)
Source: `legacy/contoso/Models/SchoolViewModels/AssignedCourseData.cs:3`

| Field | Type | Note |
|---|---|---|
| CourseID | int |  |
| Title | string |  |
| Assigned | bool | checkbox state; built by PopulateAssignedCourseData (Controllers/InstructorsController.cs:116-123) |

Used by: Instructor course assignments are synchronized to the selected course set, Instructor can be assigned to a given course at most once (many-to-many teachin…

## ErrorViewModel
Source: `legacy/contoso/Models/ErrorViewModel.cs:5`

| Field | Type | Note |
|---|---|---|
| RequestId | string |  |
| ShowRequestId | bool (computed) | !string.IsNullOrEmpty(RequestId) |

## Notification poll response (anonymous JSON)
Source: `legacy/contoso/Controllers/NotificationsController.cs:36`

| Field | Type | Note |
|---|---|---|
| success | bool |  |
| notifications | List<Notification> | at most 10, dequeued (destructive) from MSMQ (NotificationsController.cs:21-27) |
| count | int |  |
| message | string | only on error path (NotificationsController.cs:33) |

Used by: Notification retrieval is destructive and capped at 10 per poll, Relative time display ('time ago'), Mark-as-read is a no-op (IsRead/ReadAt lifecycle not implemented)
