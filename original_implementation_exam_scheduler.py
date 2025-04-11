"""
Schedules exams using eigenvalue decomposition of graph Laplacian.
Constraints: Max 2 exams/day per student, no direct conflicts.
"""
import random

# Parameters
num_exams = 10
num_students = 50
min_exams_per_student = 2
max_exams_per_student = 5

# Step 1: Generate student exam enrollments
student_exam_matrix = np.zeros((num_students, num_exams), dtype=int)
for student in range(num_students):
    chosen_exams = random.sample(range(num_exams), random.randint(min_exams_per_student, max_exams_per_student))
    for exam in chosen_exams:
        student_exam_matrix[student, exam] = 1

# Step 2: Conflict matrix
conflict_matrix = student_exam_matrix.T @ student_exam_matrix
np.fill_diagonal(conflict_matrix, 0)

# Step 3: Laplacian
degree_matrix = np.diag(conflict_matrix.sum(axis=1))
laplacian_matrix = degree_matrix - conflict_matrix

# Step 4: Eigenvalue decomposition
eigenvalues, eigenvectors = np.linalg.eigh(laplacian_matrix)
fiedler_vector = eigenvectors[:, 1]  # Second smallest eigenvector

# Step 5: Partition exams
group_1 = [i for i, val in enumerate(fiedler_vector) if val >= 0]
group_2 = [i for i, val in enumerate(fiedler_vector) if val < 0]

# Step 6: Distribute exams across multiple days with constraints:
# - Max 2 exams per student per day
# - Group 1 and Group 2 exams are scheduled on different days to avoid cross-group conflicts

# Let's try to alternate group exams over a number of days
# and check per student if any day exceeds 2 exams

# We'll aim for a compact schedule while obeying rules

from collections import defaultdict

# Helper: assign exams to time slots (days), alternating group 1 and 2
exam_schedule = defaultdict(list)  # day -> list of exams
day = 0
groups = [group_1, group_2]
day_assignments = {}

# Alternate placing exams from group_1 and group_2 into days
for group in groups:
    exams_remaining = group.copy()
    while exams_remaining:
        # Assign up to 2 exams per day from this group
        exams_today = exams_remaining[:2]
        exam_schedule[day].extend(exams_today)
        for exam in exams_today:
            day_assignments[exam] = day
        exams_remaining = exams_remaining[2:]
        day += 1  # go to next day

# Step 7: Check if any student has more than 2 exams per day
# Create a reverse mapping: student -> day -> exams
student_day_count = np.zeros((num_students, day), dtype=int)

for student in range(num_students):
    for exam in range(num_exams):
        if student_exam_matrix[student, exam]:
            assigned_day = day_assignments.get(exam, -1)
            if assigned_day != -1:
                student_day_count[student, assigned_day] += 1

# Count violations: students with more than 2 exams per day
violations = (student_day_count > 2).sum()

exam_schedule, violations

# Prepare visualization
fig, ax = plt.subplots(figsize=(10, 4))
colors = plt.cm.tab10.colors

# Plot exam blocks by day
for day, exams in exam_schedule.items():
    for i, exam in enumerate(exams):
        ax.barh(y=day, width=1, left=i, height=0.6, color=colors[exam % len(colors)], edgecolor='black')
        ax.text(i + 0.5, day, f'Exam {exam}', va='center', ha='center', fontsize=9, color='white')

# Formatting
ax.set_yticks(list(exam_schedule.keys()))
ax.set_yticklabels([f'Day {d}' for d in exam_schedule.keys()])
ax.set_xlabel('Exam Slots (Max 2 per Day)')
ax.set_title('📅 Exam Schedule Visualization')
ax.invert_yaxis()
ax.set_xlim(0, 3)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
