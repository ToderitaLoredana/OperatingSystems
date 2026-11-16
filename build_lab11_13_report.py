from pathlib import Path
import shutil

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "reports" / "labs11-13"
ASSETS = OUT / "assets"
DOCX = OUT / "Labs11-13_Report_Tacu_Loredana_FAF-242.docx"

SCREENSHOTS = {
    "race": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-7f764d38-a8d4-4320-af97-64a59bc583bb.png"),
    "locks": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-f0982a44-7dd6-40d9-88ef-86f79652489f.png"),
    "timing": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-0a639e1c-191b-4587-9dd2-937ed60e6d84.png"),
    "order_parking": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-ed4b55c0-1ec2-4d0a-bea3-1a9009dd00c5.png"),
    "prodcons": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-03a076be-04d1-4b5b-a24a-7d773d77bdfb.png"),
    "cond_readers": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-1e9233d3-d2cd-4b86-a756-6e9139d03069.png"),
    "deadlock": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-cfb2fefd-c4a5-457c-a00a-47c9baafdc28.png"),
    "mix": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-73f41c55-1767-4a38-b38c-dc4d0dfb7761.png"),
    "mix_lock": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-f0faebef-2dd2-49a2-b700-d1721453672a.png"),
    "semtest": Path("/var/folders/hz/chwbvcls1r99dpvrjy2gk5qh0000gn/T/codex-clipboard-3143e945-fb5a-47c8-bee0-54d3b9ea3032.png"),
}


def set_font(run, name="Arial", size=11, bold=False, italic=False, color="000000"):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor.from_string(color)
    rpr = run._element.get_or_add_rPr()
    rpr.rFonts.set(qn("w:ascii"), name)
    rpr.rFonts.set(qn("w:hAnsi"), name)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = tcpr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcpr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=110, bottom=100, end=110):
    tcpr = cell._tc.get_or_add_tcPr()
    tc_mar = tcpr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tcpr.append(tc_mar)
    for name, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def table_borders(table, color="D9D9D9", size="6"):
    tblpr = table._tbl.tblPr
    borders = tblpr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tblpr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:color"), color)


def prevent_row_split(row):
    row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def repeat_header(row):
    hdr = OxmlElement("w:tblHeader")
    hdr.set(qn("w:val"), "true")
    row._tr.get_or_add_trPr().append(hdr)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)


def configure_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.0)
    section.different_first_page_header_footer = True
    add_page_number(section.footer.paragraphs[0])

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(7)
    normal.paragraph_format.line_spacing = 1.08

    title = doc.styles["Title"]
    title.font.name = "Arial"
    title.font.size = Pt(20)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)
    title_ppr = title._element.get_or_add_pPr()
    border = title_ppr.find(qn("w:pBdr"))
    if border is not None:
        title_ppr.remove(border)

    for level, size in ((1, 15), (2, 13), (3, 11.5)):
        style = doc.styles[f"Heading {level}"]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.keep_with_next = True

    caption = doc.styles["Caption"]
    caption.font.name = "Arial"
    caption.font.size = Pt(9)
    caption.font.italic = True
    caption.font.color.rgb = RGBColor(0, 0, 0)

    doc.core_properties.title = "Laboratory Works 11 12 and 13 Synchronization and Semaphores"
    doc.core_properties.author = "Tacu Loredana"
    doc.core_properties.subject = "Operating Systems"


def add_cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(5)
    p.add_run().add_picture(str(ROOT / "report_assets" / "utm_logo.png"), width=Inches(1.0))

    for text in (
        "MINISTRY OF EDUCATION AND RESEARCH OF THE REPUBLIC OF MOLDOVA",
        "Technical University of Moldova",
        "Faculty of Computers Informatics and Microelectronics",
        "Department of Software Engineering and Automation",
    ):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
        set_font(p.add_run(text), size=11, bold=True)

    doc.add_paragraph()
    p = doc.add_paragraph()
    set_font(p.add_run("Student:\nTacu Loredana\nFAF-242"), size=11, bold=True)
    p.paragraph_format.space_after = Pt(12)

    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("REPORT")

    for text, size, bold, italic in (
        ("Laboratory Works No 11 No 12 and No 13", 14, True, False),
        ("Thread Synchronization and Kernel Semaphores", 13, True, False),
        ("Operating Systems", 12, False, True),
    ):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(4)
        set_font(p.add_run(text), size=size, bold=bold, italic=italic)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_font(p.add_run("Checked by:\nUniversitary Assistant\nReițman Patricia"), size=11, bold=True)

    for _ in range(3):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(p.add_run("Chișinău 2026"), size=11, bold=True)
    doc.add_page_break()


def add_heading(doc, text, level=1):
    return doc.add_paragraph(text, style=f"Heading {level}")


def add_body(doc, text, bold_lead=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_lead:
        set_font(p.add_run(bold_lead), bold=True)
    set_font(p.add_run(text))
    return p


def add_commands(doc, lines):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.right_indent = Cm(0.4)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.keep_together = True
    p.paragraph_format.keep_with_next = True
    for index, line in enumerate(lines):
        run = p.add_run(("\n" if index else "") + line)
        set_font(run, name="Courier New", size=9.5)


def add_figure(doc, key, caption, width=6.15):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(ASSETS / f"{key}.png"), width=Inches(width))
    cap = doc.add_paragraph(caption, style="Caption")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    return cap


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table_borders(table)
    header = table.rows[0]
    repeat_header(header)
    for index, text in enumerate(headers):
        cell = header.cells[index]
        shade(cell, "404040")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p.add_run(text), size=9.5, bold=True, color="FFFFFF")
        if widths:
            cell.width = Cm(widths[index])
    for row_index, row_data in enumerate(rows):
        row = table.add_row()
        prevent_row_split(row)
        for index, text in enumerate(row_data):
            cell = row.cells[index]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins(cell)
            if row_index % 2:
                shade(cell, "F5F5F5")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if index else WD_ALIGN_PARAGRAPH.CENTER
            set_font(p.add_run(str(text)), size=9.3)
            if widths:
                cell.width = Cm(widths[index])
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def prepare_assets():
    OUT.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    for key, source in SCREENSHOTS.items():
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, ASSETS / f"{key}.png")


def build():
    prepare_assets()
    doc = Document()
    configure_document(doc)
    add_cover(doc)

    add_heading(doc, "1 Purpose of the Laboratory Works")
    add_body(doc, "Laboratory Work No 11 demonstrates race conditions and three uses of a POSIX semaphore: mutual exclusion, event signaling, and resource counting. Laboratory Work No 12 combines semaphores, mutexes, and condition variables in the producer-consumer, readers-writers, and deadlock problems. Laboratory Work No 13 implements counting semaphores inside xv6 as three system calls and validates process synchronization in the teaching kernel.")

    add_heading(doc, "2 Objectives")
    objectives = (
        "Observe lost updates when two threads modify a shared counter without synchronization.",
        "Protect critical sections with a mutex, a binary semaphore, and an atomic operation.",
        "Use semaphores to enforce execution order and limit access to a finite resource.",
        "Coordinate a bounded buffer with empty and full semaphores and a mutex.",
        "Apply a condition variable and explain why its predicate is checked in a loop.",
        "Allow concurrent readers while keeping writers mutually exclusive.",
        "Create a circular-wait deadlock and remove it with a consistent lock order.",
        "Add sem_init, sem_down, and sem_up to xv6 and verify blocking and mutual exclusion.",
    )
    for index, item in enumerate(objectives, 1):
        p = doc.add_paragraph(style="List Number")
        set_font(p.add_run(item))

    add_heading(doc, "3 Theoretical Background")
    add_body(doc, "A race condition occurs when the result depends on the order in which concurrent operations execute. The expression counter++ is a load, an addition, and a store. If two threads load the same value before either stores its result, both may write the same incremented value and one addition is lost.")
    add_body(doc, "A mutex allows one thread at a time to enter a critical section. A semaphore generalizes this idea with a nonnegative permit count. sem_wait consumes a permit or blocks when the count is zero, while sem_post returns a permit and wakes a waiter. An initial value of one provides mutual exclusion, zero represents an unavailable event, and a larger value counts available resources.")
    add_body(doc, "Condition variables let a thread sleep until shared state may have changed. The state remains in an ordinary variable protected by a mutex, so the waiting thread must recheck the predicate after every wakeup. Deadlock arises when threads hold resources while waiting in a cycle. Requiring every thread to acquire locks in the same order removes circular wait.")
    add_body(doc, "Inside xv6, a semaphore combines an integer value, a spinlock that protects the value, and the kernel sleep and wakeup mechanism. A process waiting at zero releases the spinlock before sleeping so sem_up can acquire the lock, increment the value, and wake blocked processes.")

    heading = add_heading(doc, "4 Laboratory Work No 11 The Race and the Semaphore")
    heading.paragraph_format.page_break_before = True
    add_heading(doc, "4.1 Observing the Race Condition", 2)
    add_commands(doc, ["./bin/race", "./bin/race", "./bin/race"])
    add_figure(doc, "race", "Figure 1 - Three executions of the unprotected shared counter")
    add_body(doc, "The three runs produced 1,064,758, 1,023,333, and 1,144,796 instead of 2,000,000. Both threads repeatedly loaded the same counter value, incremented their private register values, and stored identical results. Scheduling and instruction interleaving changed between runs, so the number of lost updates also changed.", "Observation. ")

    add_heading(doc, "4.2 Mutual Exclusion and Synchronization Cost", 2)
    add_commands(doc, ["./bin/mutex; ./bin/mutex; ./bin/mutex", "./bin/sem; ./bin/sem; ./bin/sem"])
    add_figure(doc, "locks", "Figure 2 - Correct counter results with a mutex and a semaphore")
    add_body(doc, "Every mutex and semaphore run returned 2,000,000. A semaphore initialized to one admits only one thread to counter++ at a time. Initializing it to two would admit both worker threads and reintroduce lost updates, so it would no longer act as a mutual-exclusion lock.", "Observation. ")

    add_commands(doc, ["time ./bin/race", "time ./bin/mutex", "time ./bin/sem"])
    add_figure(doc, "timing", "Figure 3 - Timing comparison for unprotected and protected counters")
    add_table(doc, ["Program", "Result", "Real time"], [
        ("race", "1,096,446 incorrect", "0.019 s"),
        ("mutex", "2,000,000 correct", "0.049 s"),
        ("semaphore", "2,000,000 correct", "0.028 s"),
    ], widths=[3.4, 7.0, 3.0])
    add_body(doc, "The protected programs perform synchronization around every increment. Atomic lock operations, cache-coherence traffic, and possible waiting add overhead. Exact timings and the relative order of mutex and semaphore results depend on the machine and scheduler.")

    add_heading(doc, "4.3 Signaling Counting and Atomic Operations", 2)
    add_commands(doc, ["./bin/order", "./bin/parking", "time ./bin/atomic"])
    add_figure(doc, "order_parking", "Figure 4 - Semaphore signaling parking capacity and atomic increments")
    add_body(doc, "The ready semaphore started at zero, so the reader printed its waiting message and blocked until the writer stored hello and posted the semaphore. If ready started at one, the reader could pass before the write and read the initially empty global array. An initial value of zero therefore means that no operation may pass until another thread signals it.", "Signaling observation. ")
    add_body(doc, "The parking count never exceeded three because every car executed sem_wait before incrementing inside. Setting PLACES to one would turn the counter into a binary semaphore and serialize the cars. The optional atomic counter also reached 2,000,000 because atomic_fetch_add performs the update indivisibly.", "Counting observation. ")

    add_heading(doc, "4.4 Laboratory Work No 11 Results", 2)
    add_body(doc, "The experiments connected the abstract idea of a race to visible lost updates. Mutual exclusion repaired the counter, a zero-valued semaphore enforced order, a counting semaphore limited occupancy, and an atomic operation protected a single numeric update without an explicit lock.")

    heading = add_heading(doc, "5 Laboratory Work No 12 Producer Consumer and the Other Tools")
    heading.paragraph_format.page_break_before = True
    add_heading(doc, "5.1 Producer and Consumer", 2)
    add_commands(doc, ["./bin/prodcons"])
    add_figure(doc, "prodcons", "Figure 5 - Bounded producer-consumer buffer")
    add_body(doc, "The producer filled the four slots and then waited in sem_wait(&empty). The consumer initially waited in sem_wait(&full) because full started at zero. The displayed count never exceeded four and returned to zero after item 8 was consumed.", "Observation. ")
    add_body(doc, "Moving pthread_mutex_lock before the producer's sem_wait would create a deadlock when the buffer became full. The producer would sleep while holding the buffer mutex, and the consumer could not acquire that mutex to remove an item and post empty.")

    add_heading(doc, "5.2 Condition Variable and Readers Writers", 2)
    add_commands(doc, ["./bin/condvar", "./bin/readers"])
    add_figure(doc, "cond_readers", "Figure 6 - Condition-variable ordering and concurrent readers")
    add_body(doc, "In condvar, the integer ready records whether the message exists. Replacing while with if usually works in this single-reader demonstration, but while is required because a condition wait may wake spuriously or another thread may change the predicate before the awakened thread reacquires the mutex.", "Condition-variable observation. ")
    add_body(doc, "The first reader increments readers and waits on room, excluding writers. The last reader decrements readers to zero and posts room. The separate rlock semaphore makes those counter transitions atomic. Without it, lost updates could cause incorrect first-reader or last-reader decisions. A continuous stream of readers can keep room occupied and starve a waiting writer.", "Readers-writers observation. ")

    add_heading(doc, "5.3 Deadlock and Consistent Lock Ordering", 2)
    add_commands(doc, ["timeout 5 ./bin/deadlock-original", "timeout 5 ./bin/deadlock"])
    add_figure(doc, "deadlock", "Figure 7 - Circular wait and the corrected lock order")
    add_body(doc, "In the original program, thread one held A and waited for B while thread two held B and waited for A. The circle one to B to two to A to one prevented either thread from progressing, and timeout returned 124. Removing the sleeps would only make the failure intermittent because one thread might sometimes acquire both locks first.", "Observation. ")
    add_body(doc, "The corrected version made both threads acquire A before B. It printed both critical-section messages, reached done, and returned exit code 0. A common acquisition order prevents a thread from holding a later lock while waiting for an earlier one, so circular wait cannot form.")

    add_heading(doc, "5.4 Laboratory Work No 12 Results", 2)
    add_body(doc, "The bounded buffer demonstrated how resource-counting semaphores and a mutex solve different parts of one problem. The condition-variable example separated shared state from the sleeping mechanism, the readers-writers solution admitted concurrent readers, and the deadlock experiment showed why lock ordering is part of a correct synchronization design.")

    add_heading(doc, "6 Laboratory Work No 13 Semaphores in the xv6 Kernel")
    add_heading(doc, "6.1 Implementation Path", 2)
    add_body(doc, "The xv6 implementation added system calls 24, 25, and 26. The user declarations and generated ecall stubs expose the calls, the dispatch table maps their numbers to kernel handlers, and kernel/sem.c stores eight system-wide semaphores.")
    add_table(doc, ["File", "Implemented element", "Purpose"], [
        ("kernel/syscall.h", "SYS_sem_init 24, SYS_sem_down 25, SYS_sem_up 26", "Assigns system-call numbers"),
        ("user/user.h", "Three function declarations", "Defines the user interface"),
        ("user/usys.pl", "Three generated stubs", "Executes ecall with each number"),
        ("kernel/syscall.c", "Declarations and dispatch entries", "Routes calls to kernel handlers"),
        ("kernel/sem.c", "Value, spinlock, sleep, and wakeup", "Implements counting semaphores"),
        ("user/semtest.c", "Order and ping-pong tests", "Validates blocking and alternation"),
        ("user/mix.c", "Unlocked and locked output", "Validates mutual exclusion"),
        ("Makefile", "sem.o, semtest, and mix", "Builds the kernel and user programs"),
    ], widths=[4.0, 6.8, 5.0])

    add_heading(doc, "6.2 Blocking and Alternation", 2)
    add_commands(doc, ["$ semtest"])
    add_figure(doc, "semtest", "Figure 8 - xv6 semaphore order and ping-pong tests")
    add_body(doc, "Semaphore 0 started at zero, so the child slept in sem_down until the parent posted after ten ticks. Semaphores 1 and 2 then passed execution between the parent and child, producing three strictly alternating ping-pong pairs and semtest: OK.", "Observation. ")
    add_body(doc, "sem_down checks the value with while rather than if because sem_up wakes all processes sleeping on the semaphore address. One process may take the available unit before another awakened process reacquires the spinlock, leaving the value at zero again.")

    add_heading(doc, "6.3 Semaphore as a Kernel Lock", 2)
    add_commands(doc, ["$ mix", "$ mix lock"])
    add_figure(doc, "mix", "Figure 9 - Character-level interleaving without a semaphore lock")
    add_figure(doc, "mix_lock", "Figure 10 - Complete lines protected by semaphore 3")
    add_body(doc, "Without locking, each 30-character line plus its newline required 31 write system calls. The scheduler could switch processes between calls, so A and b characters mixed. sem_down(3) before the character loop and sem_up(3) after it made each complete line a critical section.", "Observation. ")
    add_body(doc, "sem_down releases the semaphore spinlock before calling sleep. If a process slept while holding the spinlock, sem_up could never acquire it to increment the value and wake the waiter, so the semaphore would deadlock.")

    add_heading(doc, "6.4 Laboratory Work No 13 Results", 2)
    add_body(doc, "The kernel semaphore implementation compiled into xv6 and passed both functional tests. semtest confirmed blocking and strict alternation, while mix showed the difference between unprotected system calls and a line-sized critical section.")

    add_heading(doc, "7 Comparison of Synchronization Mechanisms")
    add_table(doc, ["Mechanism", "State or capacity", "Primary use", "Observed example"], [
        ("Mutex", "Locked or unlocked", "One thread in a critical section", "Correct shared counter"),
        ("Binary semaphore", "0 or 1 permit", "Lock or one-time signal", "Counter lock and message order"),
        ("Counting semaphore", "Several permits", "Bounded resources", "Parking spaces and buffer slots"),
        ("Condition variable", "Predicate stored separately", "Sleep until shared state changes", "Message readiness"),
        ("Atomic operation", "Single indivisible update", "Simple numeric state", "Atomic shared counter"),
        ("xv6 kernel semaphore", "Kernel value and wait channel", "Process synchronization", "semtest and mix"),
    ], widths=[3.4, 4.1, 4.5, 4.6])

    add_heading(doc, "8 Conclusions")
    add_body(doc, "The laboratory works demonstrated that correct concurrent code requires protection for both shared data and execution order. An unprotected counter lost updates, while mutexes, semaphores, and atomic operations preserved the expected value. Counting semaphores represented finite capacity in the parking and bounded-buffer experiments, and a zero-valued semaphore represented an event that had not yet occurred.")
    add_body(doc, "The producer-consumer, condition-variable, readers-writers, and deadlock experiments showed that synchronization primitives must be combined with a precise invariant. Waiting while holding the wrong mutex caused deadlock, checking a condition only once was unsafe, and inconsistent lock order created circular wait.")
    add_body(doc, "Implementing semaphores in xv6 connected the user-level operations to kernel mechanisms. The final system calls protected the permit count with a spinlock, released the lock before sleeping, and used wakeup on the same semaphore address. The successful semtest and mix runs confirmed both blocking and mutual exclusion.")

    add_heading(doc, "9 References")
    refs = (
        "Operating Systems Laboratory Work No 11 The Race and the Semaphore FCIM FAF UTM 2026",
        "Operating Systems Laboratory Work No 12 Producer Consumer and the Other Tools FCIM FAF UTM 2026",
        "Operating Systems Laboratory Work No 13 Semaphores in Your Own Kernel FCIM FAF UTM 2026",
        "MIT PDOS xv6 riscv source tree https://github.com/mit-pdos/xv6-riscv",
        "The Open Group POSIX Threads and Semaphores specifications https://pubs.opengroup.org/onlinepubs/9699919799/",
    )
    for index, ref in enumerate(refs, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        set_font(p.add_run(f"{index}. {ref}"), size=10)

    doc.save(DOCX)
    print(DOCX)


if __name__ == "__main__":
    build()
