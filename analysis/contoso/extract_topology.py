#!/usr/bin/env python
"""Extract the dependency/topology map of legacy/contoso (ASP.NET MVC 5 + EF Core 3.1).

Run from the repo root:  python analysis/contoso/extract_topology.py
Writes analysis/contoso/topology.json and prints a summary.

Edge sources:
  call      C# type references (class names used in another file), base-class inheritance,
            layout -> script/bundle includes
  dispatch  MVC convention routing (RouteConfig -> every controller), controller -> its
            Views/<Name>/ folder (View() convention), Html.ActionLink/BeginForm targets,
            fetch('/Controller/Action') URLs in first-party JS
  read      db.<DbSet> usage, .Include/.ThenInclude navigations, ConfigurationManager,
            MSMQ Receive, <img src> of uploaded files
  write     db.<DbSet>.Add/Remove, db.Entry(x).State on typed params, TryUpdateModel,
            navigation collection Add, seed Add, MSMQ Send, file SaveAs/Delete
Lines the regexes cannot see are listed in MANUAL_EDGES, each with a source citation.
"""
import json, os, re, sys
from collections import defaultdict

ROOT = os.path.join("legacy", "contoso")
OUT = os.path.join("analysis", "contoso", "topology.json")

# ---------------------------------------------------------------- node catalogue
# (id, domain, kind, path relative to ROOT; a directory for view folders)
DOMAINS = {
    "platform": "Startup and Shell",
    "data": "Data Access",
    "students": "Students",
    "courses": "Courses and Uploads",
    "faculty": "Instructors and Departments",
    "notifications": "Notifications (MSMQ)",
    "home": "Home and Reporting",
    "stores": "Data stores",
}
NODES = [
    ("Global.asax.cs", "platform", "module", "Global.asax.cs"),
    ("RouteConfig", "platform", "module", "App_Start/RouteConfig.cs"),
    ("FilterConfig", "platform", "module", "App_Start/FilterConfig.cs"),
    ("BundleConfig", "platform", "module", "App_Start/BundleConfig.cs"),
    ("Web.config", "platform", "module", "Web.config"),
    ("BaseController", "platform", "module", "Controllers/BaseController.cs"),
    ("Views/Shared", "platform", "screen", "Views/Shared"),
    ("ErrorViewModel", "platform", "module", "Models/ErrorViewModel.cs"),
    ("LoggingService", "platform", "module", "Services/LoggingService.cs"),
    ("SchoolContext", "data", "module", "Data/SchoolContext.cs"),
    ("SchoolContextFactory", "data", "module", "Data/SchoolContextFactory.cs"),
    ("DbInitializer", "data", "module", "Data/DbInitializer.cs"),
    ("PaginatedList", "data", "module", "PaginatedList.cs"),
    ("Person", "data", "module", "Models/Person.cs"),
    ("StudentsController", "students", "module", "Controllers/StudentsController.cs"),
    ("Views/Students", "students", "screen", "Views/Students"),
    ("Student", "students", "module", "Models/Student.cs"),
    ("Enrollment", "students", "module", "Models/Enrollment.cs"),
    ("CoursesController", "courses", "module", "Controllers/CoursesController.cs"),
    ("Views/Courses", "courses", "screen", "Views/Courses"),
    ("Course", "courses", "module", "Models/Course.cs"),
    ("InstructorsController", "faculty", "module", "Controllers/InstructorsController.cs"),
    ("DepartmentsController", "faculty", "module", "Controllers/DepartmentsController.cs"),
    ("Views/Instructors", "faculty", "screen", "Views/Instructors"),
    ("Views/Departments", "faculty", "screen", "Views/Departments"),
    ("Instructor", "faculty", "module", "Models/Instructor.cs"),
    ("Department", "faculty", "module", "Models/Department.cs"),
    ("OfficeAssignment", "faculty", "module", "Models/OfficeAssignment.cs"),
    ("CourseAssignment", "faculty", "module", "Models/CourseAssignment.cs"),
    ("InstructorIndexData", "faculty", "module", "Models/SchoolViewModels/InstructorIndexData.cs"),
    ("AssignedCourseData", "faculty", "module", "Models/SchoolViewModels/AssignedCourseData.cs"),
    ("NotificationService", "notifications", "module", "Services/NotificationService.cs"),
    ("NotificationsController", "notifications", "module", "Controllers/NotificationsController.cs"),
    ("Views/Notifications", "notifications", "screen", "Views/Notifications"),
    ("notifications.js", "notifications", "module", "Scripts/notifications.js"),
    ("Notification", "notifications", "module", "Models/Notification.cs"),
    ("HomeController", "home", "module", "Controllers/HomeController.cs"),
    ("Views/Home", "home", "screen", "Views/Home"),
    ("EnrollmentDateGroup", "home", "module", "Models/SchoolViewModels/EnrollmentDateGroup.cs"),
]
TABLES = ["Person", "Course", "Department", "Enrollment", "CourseAssignment",
          "OfficeAssignment", "Notification"]
STORES = [("ds:" + t, f"SQL table {t}") for t in TABLES] + [
    ("ds:MSMQ:ContosoUniversityNotifications", "MSMQ private queue ContosoUniversityNotifications"),
    ("ds:Disk:Uploads/TeachingMaterials", "Disk folder ~/Uploads/TeachingMaterials"),
]
DBSET_TABLE = {"Students": "Person", "Instructors": "Person", "People": "Person",
               "Courses": "Course", "Departments": "Department", "Enrollments": "Enrollment",
               "OfficeAssignments": "OfficeAssignment", "CourseAssignments": "CourseAssignment",
               "Notifications": "Notification"}
NAV_TABLE = {"Department": "Department", "Administrator": "Person", "OfficeAssignment": "OfficeAssignment",
             "CourseAssignments": "CourseAssignment", "Course": "Course", "Enrollments": "Enrollment",
             "Student": "Person", "Instructor": "Person"}
ENTITY_TABLE = {"Student": "Person", "Instructor": "Person", "Course": "Course",
                "Department": "Department"}

# Edges the regexes cannot see. Each cites the line that proves it.
MANUAL_EDGES = [
    # InstructorsController.cs:241  department.InstructorID = null (instructor delete clears dept admin)
    ("InstructorsController", "ds:Department", "write"),
    # InstructorsController.cs:156  instructorToUpdate.OfficeAssignment = null; Location bound via TryUpdateModel
    ("InstructorsController", "ds:OfficeAssignment", "write"),
    # InstructorsController.cs:203  db.Entry(courseToRemove).State = EntityState.Deleted
    ("InstructorsController", "ds:CourseAssignment", "write"),
    # Views/Courses/*.cshtml  <img src="@Url.Content(item.TeachingMaterialImagePath)"> serves uploads
    ("Views/Courses", "ds:Disk:Uploads/TeachingMaterials", "read"),
]

# ---------------------------------------------------------------- helpers
def path(p): return os.path.join(ROOT, p)

def read(p):
    with open(p, encoding="utf-8-sig", errors="replace") as f:
        return f.read()

def strip_cs_comments(src):
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//[^\n]*", "", src)

def loc_of(rel):
    p = path(rel)
    files = []
    if os.path.isdir(p):
        for dp, _, fns in os.walk(p):
            files += [os.path.join(dp, f) for f in fns if f.endswith(".cshtml")]
    else:
        files = [p]
    return sum(1 for f in files for l in read(f).splitlines() if l.strip())

def view_sources(rel):
    p = path(rel)
    out = {}
    for fn in sorted(os.listdir(p)):
        if fn.endswith(".cshtml"):
            out[fn] = read(os.path.join(p, fn))
    return out

def methods(src):
    """Split C# source into (name, body) by brace matching after a method signature."""
    res = []
    for m in re.finditer(r"(?:public|private|protected)\s+[\w<>\[\],\s]+?\s(\w+)\s*\(([^)]*)\)\s*\{", src):
        i, depth = m.end(), 1
        while i < len(src) and depth:
            depth += {"{": 1, "}": -1}.get(src[i], 0)
            i += 1
        res.append((m.group(1), m.group(2), src[m.end():i]))
    return res

# ---------------------------------------------------------------- extraction
edges = set()
def add(s, t, k):
    if s != t:
        edges.add((s, t, k))

ids = {n[0] for n in NODES}
by_id = {n[0]: n for n in NODES}
cs_nodes = {nid: rel for nid, _, _, rel in NODES if rel.endswith(".cs")}
class_names = {nid for nid in cs_nodes if nid != "Global.asax.cs"}
srcs = {nid: strip_cs_comments(read(path(rel))) for nid, rel in cs_nodes.items()}
controllers = [n for n in ids if n.endswith("Controller") and n != "BaseController"]
unresolved = []

# 1. type references between C# files (call)
for nid, src in srcs.items():
    for cls in class_names:
        if cls != nid and re.search(rf"\b{re.escape(cls)}\b", src):
            add(nid, cls, "call")

# 2. controllers: view folder (dispatch), DbSet reads/writes, uploads, notifications
for c in controllers:
    src = srcs[c]
    vf = "Views/" + c[:-len("Controller")]
    if vf in ids and re.search(r"\bView\(", src):
        add(c, vf, "dispatch")
    for m in re.finditer(r"\bdb\.(\w+)", src):
        if m.group(1) in DBSET_TABLE:
            add(c, "ds:" + DBSET_TABLE[m.group(1)], "read")
    for m in re.finditer(r"\.(?:Then)?Include\(\s*\w+\s*=>\s*\w+\.(\w+)", src):
        if m.group(1) in NAV_TABLE:
            add(c, "ds:" + NAV_TABLE[m.group(1)], "read")
    for m in re.finditer(r"\bdb\.(\w+)\.(Add|Remove)\(", src):
        add(c, "ds:" + DBSET_TABLE[m.group(1)], "write")
    for m in re.finditer(r"\.(CourseAssignments|Enrollments)\.Add\(", src):
        add(c, "ds:" + DBSET_TABLE[m.group(1)], "write")
    for name, params, body in methods(src):
        if "db.Entry(" in body:
            for ptype in re.findall(r"\]?\s*(\w+)\s+\w+\s*(?:,|$)", params):
                if ptype in ENTITY_TABLE:
                    add(c, "ds:" + ENTITY_TABLE[ptype], "write")
        if "TryUpdateModel(" in body:
            sets = re.findall(r"\bdb\.(\w+)", body)
            if sets:
                add(c, "ds:" + DBSET_TABLE[sets[0]], "write")
    if re.search(r"\.SaveAs\(|File\.Delete\(", src):
        add(c, "ds:Disk:Uploads/TeachingMaterials", "write")
    if "SendEntityNotification(" in src:
        add(c, "NotificationService", "call")

# 3. BaseController wiring (factory + per-request service instance)
if "SchoolContextFactory.Create()" in srcs["BaseController"]:
    add("BaseController", "SchoolContextFactory", "call")
add("SchoolContextFactory", "SchoolContext", "call")
for c in controllers:
    if re.search(r":\s*BaseController\b", srcs[c]):
        add(c, "BaseController", "call")

# 4. NotificationService <-> MSMQ, config reads
ns = srcs["NotificationService"]
if re.search(r"_queue\.Send\(", ns):
    add("NotificationService", "ds:MSMQ:ContosoUniversityNotifications", "write")
if re.search(r"_queue\.Receive\(", ns):
    add("NotificationService", "ds:MSMQ:ContosoUniversityNotifications", "read")
for nid, src in srcs.items():
    if "ConfigurationManager" in src:
        add(nid, "Web.config", "read")
if "ReceiveNotification(" in srcs["NotificationsController"]:
    add("NotificationsController", "NotificationService", "call")

# 5. seed writes
for m in re.finditer(r"context\.(\w+)\.(Add|AddRange)\(", srcs["DbInitializer"]):
    add("DbInitializer", "ds:" + DBSET_TABLE[m.group(1)], "write")
if "EnsureCreated" in srcs["DbInitializer"]:
    add("DbInitializer", "SchoolContext", "call")

# 6. Global.asax startup sequence
ga = srcs["Global.asax.cs"]
for cfg in ("RouteConfig", "FilterConfig", "BundleConfig", "DbInitializer", "SchoolContext"):
    if re.search(rf"\b{cfg}\b", ga):
        add("Global.asax.cs", cfg, "call")

# 7. Routing: single convention route {controller}/{action}/{id} reaches every controller
if "{controller}/{action}/{id}" in read(path("App_Start/RouteConfig.cs")):
    for c in controllers:
        add("RouteConfig", c, "dispatch")

# 8. Views: ActionLink / BeginForm / Url.Action targets, layout includes
ctrl_by_short = {c[:-len("Controller")]: c for c in controllers}
for vid in [n for n in ids if n.startswith("Views/")]:
    own = ctrl_by_short.get(vid.split("/")[1])
    for fn, vs in view_sources(vid).items():
        for m in re.finditer(r'(?:ActionLink\("[^"]*",\s*"\w+",\s*"(\w+)"|BeginForm\("\w+",\s*"(\w+)"|Url\.Action\("\w+",\s*"(\w+)")', vs):
            tgt = ctrl_by_short.get(next(g for g in m.groups() if g))
            if tgt:
                add(vid, tgt, "dispatch")
        if own and re.search(r"BeginForm\(|ActionLink\(", vs):
            add(vid, own, "dispatch")
        if re.search(r"Scripts\.Render|Styles\.Render", vs):
            add(vid, "BundleConfig", "call")
        if "notifications.js" in vs:
            add(vid, "notifications.js", "call")
        if vid == "Views/Shared" and "HandleErrorInfo" in vs:
            add("FilterConfig", "Views/Shared", "dispatch")  # HandleErrorAttribute renders Shared/Error

# 9. first-party JS fetch URLs
js = read(path("Scripts/notifications.js"))
for m in re.finditer(r"""(?:fetch|\$\.(?:get|post|ajax|getJSON))\(\s*['"]/(\w+)/(\w+)""", js):
    tgt = ctrl_by_short.get(m.group(1))
    if tgt:
        add("notifications.js", tgt, "dispatch")
    else:
        unresolved.append(f"notifications.js -> /{m.group(1)}/{m.group(2)}")

for s, t, k in MANUAL_EDGES:
    add(s, t, k)

# ---------------------------------------------------------------- entry points, dead ends
entry = ["Global.asax.cs", "notifications.js"] + sorted(controllers)
store_ids = {s for s, _ in STORES}
inbound = defaultdict(int)
for s, t, k in edges:
    inbound[t] += 1
dead = sorted(n for n in ids if n not in entry and inbound[n] == 0)
dead_stores = sorted(s for s in store_ids if not any(t == s and k == "write" for _, t, k in edges))

# Convention-based dispatch that this map cannot rule out as a target
reflection_sites = []
for nid, src in srcs.items():
    for pat in (r"GetEntityTypes\(\)", r"Activator\.CreateInstance", r"Type\.GetType\(", r"typeof\("):
        n = len(re.findall(pat, src))
        if n:
            reflection_sites.append(f"{nid}: {pat.replace(chr(92), '')} x{n}")

# ---------------------------------------------------------------- assemble
def leaf(nid, dom, kind, rel):
    d = {"id": nid, "name": nid, "kind": kind, "loc": loc_of(rel), "file": rel.replace("\\", "/")}
    d["language"] = {".cs": "csharp", ".js": "javascript", ".config": "xml"}.get(os.path.splitext(rel)[1], "razor")
    return d

children = []
for dom, label in DOMAINS.items():
    if dom == "stores":
        kids = [{"id": s, "name": name, "kind": "datastore"} for s, name in STORES]
    else:
        kids = [leaf(*n) for n in NODES if n[1] == dom]
    children.append({"id": f"dom:{dom}", "name": label, "kind": "domain", "children": kids})

all_leaf_ids = ids | store_ids
bad = [e for e in edges if e[0] not in all_leaf_ids or e[1] not in all_leaf_ids]
assert not bad, f"edges with unknown endpoints: {bad}"

writers = defaultdict(set)
for s, t, k in edges:
    if k == "write" and t in store_ids:
        writers[t].add(s)

observations = [
    "Every controller inherits BaseController, which creates a SchoolContext via SchoolContextFactory and a new "
    "NotificationService per request: the base class is the single coupling hub (data, messaging, error swallowing) "
    "and the natural seam for dependency injection in the rebuild.",
    "MSMQ queue ContosoUniversityNotifications has three writers (Students, Courses, Instructors/Departments via "
    "NotificationService) and one destructive reader (NotificationsController polled by notifications.js every 5 s): "
    "a single point of failure, since the NotificationService constructor runs on every request and is not guarded.",
    f"SQL table Person has {len(writers['ds:Person'])} writers ({', '.join(sorted(writers['ds:Person']))}) because "
    "Student and Instructor share one TPH table; Students and Faculty contexts must agree on its ownership when split.",
    "Instructors and Departments are tightly coupled to Courses (course-assignment checklist reads Course; instructor "
    "delete writes Department.InstructorID); Students and Home are the cleanest extraction candidates.",
    "Tables the running app never writes: "
    + ", ".join(f"{t.replace('ds:', '')} ({'seed only' if writers[t] else 'no writer at all'})"
                for t in sorted(store_ids) if t.startswith("ds:") and writers[t] <= {"DbInitializer"} and ":" not in t[3:])
    + ". Enrollment has no UI; Notification is mapped in SchoolContext but notifications live only in MSMQ.",
    "Controllers are reached by the convention route {controller}/{action}/{id} and views by the View() naming "
    "convention, not by code references; these are modelled as dispatch edges from RouteConfig and to Views/<Name>. "
    "Reflection-style call sites (no unresolved targets): " + "; ".join(reflection_sites) + ".",
]
if unresolved:
    observations.append("Unresolved dynamic targets: " + "; ".join(unresolved))

flows = [
    {"name": "Register a new student", "persona": "Registrar",
     "description": "A registrar adds a newly admitted student and administrators are told about it.",
     "steps": [
         {"label": "Open the student list from the navigation bar", "nodes": ["Views/Shared", "RouteConfig", "StudentsController"]},
         {"label": "Fill in name and enrollment date", "nodes": ["Views/Students"]},
         {"label": "Validate the date and save the student", "nodes": ["StudentsController", "BaseController", "SchoolContextFactory", "ds:Person"]},
         {"label": "Announce the new student to administrators", "nodes": ["NotificationService", "ds:MSMQ:ContosoUniversityNotifications"]},
         {"label": "Return to the paged, searchable list", "nodes": ["StudentsController", "PaginatedList", "Views/Students"]},
     ]},
    {"name": "Publish a course with its textbook image", "persona": "Department coordinator",
     "description": "A coordinator creates a course in a department and attaches a picture of the teaching material.",
     "steps": [
         {"label": "Open the new-course form with the department list", "nodes": ["CoursesController", "ds:Department", "Views/Courses"]},
         {"label": "Check the image type and size and store the file", "nodes": ["CoursesController", "ds:Disk:Uploads/TeachingMaterials"]},
         {"label": "Save the course", "nodes": ["CoursesController", "ds:Course"]},
         {"label": "Announce the new course", "nodes": ["NotificationService", "ds:MSMQ:ContosoUniversityNotifications"]},
         {"label": "Show the course list with thumbnails", "nodes": ["Views/Courses", "ds:Disk:Uploads/TeachingMaterials"]},
     ]},
    {"name": "Assign an instructor to courses and an office", "persona": "Department chair",
     "description": "A chair updates an instructor's office and the courses they teach.",
     "steps": [
         {"label": "Pick an instructor and see their courses and students", "nodes": ["InstructorsController", "InstructorIndexData", "ds:Person", "ds:CourseAssignment", "ds:Enrollment", "Views/Instructors"]},
         {"label": "Open the edit form with the course checklist", "nodes": ["InstructorsController", "AssignedCourseData", "ds:Course", "Views/Instructors"]},
         {"label": "Save office location and course assignments", "nodes": ["InstructorsController", "ds:OfficeAssignment", "ds:CourseAssignment", "ds:Person"]},
         {"label": "Announce the change", "nodes": ["NotificationService", "ds:MSMQ:ContosoUniversityNotifications"]},
     ]},
    {"name": "See live change alerts", "persona": "Administrator",
     "description": "An administrator browsing any page sees pop-up alerts when someone changes records.",
     "steps": [
         {"label": "Any page loads the alert script", "nodes": ["Views/Shared", "notifications.js"]},
         {"label": "Every 5 seconds the page asks for new alerts", "nodes": ["notifications.js", "NotificationsController"]},
         {"label": "Take up to 10 alerts off the queue", "nodes": ["NotificationService", "ds:MSMQ:ContosoUniversityNotifications"]},
         {"label": "Show each alert as a pop-up", "nodes": ["notifications.js"]},
     ]},
]
for f in flows:
    for st in f["steps"]:
        for n in st["nodes"]:
            assert n in all_leaf_ids, f"flow node {n} unknown"

topo = {
    "system": "Contoso University",
    "root": {"id": "sys", "name": "contoso", "kind": "system", "children": children},
    "edges": [{"source": s, "target": t, "kind": k} for s, t, k in sorted(edges)],
    "entryPoints": entry,
    "deadEnds": dead,
    "observations": observations,
    "flows": flows,
}

# keep descriptions from an earlier merge (describe_nodes.py) across reruns
if os.path.exists(OUT):
    old = json.load(open(OUT, encoding="utf-8"))
    desc = {}
    def walk(n):
        if "description" in n: desc[n["id"]] = n["description"]
        for c in n.get("children", []): walk(c)
    walk(old["root"])
    def put(n):
        if n["id"] in desc: n["description"] = desc[n["id"]]
        for c in n.get("children", []): put(c)
    put(topo["root"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(topo, f, indent=2)

# ---------------------------------------------------------------- summary
kinds = defaultdict(int)
for _, _, k in edges: kinds[k] += 1
print(f"wrote {OUT}")
print(f"leaves: {len(ids)} code/screen + {len(store_ids)} datastores = {len(all_leaf_ids)}")
print("edges: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())) + f" (total {len(edges)})")
print("entry points: " + ", ".join(entry))
print("dead ends: " + (", ".join(dead) or "none"))
print("stores with no writer: " + (", ".join(dead_stores) or "none"))
print("writers per store:")
for s in sorted(store_ids):
    print(f"  {s}: {', '.join(sorted(writers[s])) or '-'}")
print("unresolved dynamic targets: " + (", ".join(unresolved) or "none"))
