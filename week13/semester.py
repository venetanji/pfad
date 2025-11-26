"""Minimal harness with mocks so the original loop can execute safely."""

from __future__ import annotations

from dataclasses import dataclass
from random import choice
from time import sleep as real_sleep

ANSI_RESET = "\033[0m"
LOG_STYLES = {
    "info": ("📘", "\033[96m"),
    "progress": ("🚀", "\033[95m"),
    "success": ("✅", "\033[92m"),
    "warn": ("⚠️", "\033[93m"),
    "panic": ("💥", "\033[91m"),
    "state": ("🧠", "\033[94m"),
    "rest": ("😴", "\033[90m"),
}


def log(message: str, mood: str = "info") -> None:
    emoji, color = LOG_STYLES.get(mood, ("📘", "\033[96m"))
    print(f"{color}[semester]{ANSI_RESET} {emoji} {message}")


def sleep(seconds: int) -> None:
    hours = max(1, seconds // (60 * 60))
    for hour in range(1, hours + 1):
        log(f"Simulated rest hour {hour}/{hours}", mood="rest")
        real_sleep(1)


class SemesterClock:
    """Keeps track of how many times semester() should return 1 before ending."""

    def __init__(self, repetitions: int = 2) -> None:
        self.repetitions = repetitions

    def current(self) -> int:
        if self.repetitions > 0:
            self.repetitions -= 1
            return 1
        return 0


@dataclass
class Problem:
    difficulty: int
    solved: bool = False
    attempts: int = 0

    @classmethod
    def current(cls) -> "Problem":
        return cls(difficulty=1)

    @classmethod
    def find_harder(cls, previous: "Problem") -> "Problem":
        return cls(difficulty=previous.difficulty + 1)


class Code:
    def run(self, problem: Problem) -> bool:
        problem.attempts += 1
        # Guarantee eventual success so loops can progress.
        return problem.attempts >= 3 or choice([True, False])


class Student:
    def __init__(self) -> None:
        self.skill_level = 0

    def challenge(self, problem: Problem) -> Code:
        if choice([False, False, True]):
            raise RuntimeError("IDE froze mid-compile")
        return Code()


def reality_check() -> bool:
    return choice([True, False])


def check_state() -> str:
    return choice(["focused", "bored", "anxious"])


def skill_upgrade(student: Student) -> None:
    student.skill_level += 1


def simplify(problem: Problem) -> None:
    problem.difficulty = max(1, problem.difficulty - 1)


@dataclass
class CourseTask:
    name: str
    weight: float
    kind: str  # "assignment", "exam", "participation"
    difficulty: int | None = None
    mode: str = "individual"


COURSE_TASKS: list[CourseTask] = [
    CourseTask("Assignment 1 – Drawing Loops", 0.05, "assignment", difficulty=1),
    CourseTask("Assignment 2 – Data Journeys", 0.10, "assignment", difficulty=2),
    CourseTask("Assignment 3 – Creative Systems", 0.15, "assignment", difficulty=3),
    CourseTask(
        "Assignment 4 – Group Showcase",
        0.40,
        "assignment",
        difficulty=4,
        mode="group",
    ),
    CourseTask("Midterm Test", 0.10, "exam", difficulty=2),
    CourseTask("Final Test", 0.10, "exam", difficulty=3),
    CourseTask("Participation", 0.10, "participation"),
]


SEMESTER_CLOCK = SemesterClock(repetitions=len(COURSE_TASKS))


def semester() -> int:
    return SEMESTER_CLOCK.current()


def main() -> None:
    student = Student()
    panic = False
    earned = 0.0
    total_tasks = len(COURSE_TASKS)
    log("Starting Week 13 back-to-basics simulation", mood="progress")

    task_index = 0
    while semester() == 1 and task_index < total_tasks:
        task = COURSE_TASKS[task_index]
        log(
            f"Task {task_index + 1}/{total_tasks}: {task.name} "
            f"({task.weight * 100:.0f}% {task.mode})",
            mood="progress",
        )

        if task.kind == "assignment":
            problem = Problem(difficulty=task.difficulty or 1)
            while not problem.solved:
                try:
                    code = student.challenge(problem)
                    problem.solved = code.run(problem)
                    outcome = "solved" if problem.solved else "keep trying"
                    log(
                        "Attempt %s on difficulty %s: %s"
                        % (problem.attempts, problem.difficulty, outcome),
                        mood="info",
                    )
                except Exception as err:
                    panic = reality_check()
                    if panic:
                        log(
                            f"Runtime error '{err}'. PANIC mode engaged — phone a friend!",
                            mood="panic",
                        )
                    else:
                        log(
                            f"Runtime error '{err}'. Deep breath, keep iterating.",
                            mood="warn",
                        )
                    continue

                if problem.solved:
                    break

                state = check_state()
                log(
                    "Student state=%s, skill_level=%s, difficulty=%s"
                    % (state, student.skill_level, problem.difficulty),
                    mood="state",
                )
                if state == "bored":
                    problem.difficulty += 1
                    log(
                        f"Adding optional complexity: difficulty {problem.difficulty}",
                        mood="success",
                    )
                elif state == "anxious" or panic:
                    log("Addressing anxiety/panic with skill work", mood="warn")
                    try:
                        skill_upgrade(student)
                        log(
                            f"Skill level increased to {student.skill_level}",
                            mood="success",
                        )
                    except Exception as err:
                        log(
                            f"Skill upgrade failed: {err}. Simplifying problem",
                            mood="panic",
                        )
                        simplify(problem)
                        log(
                            f"Problem simplified to difficulty {problem.difficulty}",
                            mood="warn",
                        )
                    finally:
                        log("Taking a reset break (8h simulated)", mood="rest")
                        sleep(8 * 60 * 60)
                        panic = not panic
                        log(f"Panic toggled to {panic}", mood="state")

            earned += task.weight
            log(
                f"Submitted {task.name}! +{task.weight * 100:.0f}% (Total {earned * 100:.1f}%)",
                mood="success",
            )
            panic = False

        elif task.kind == "exam":
            attempts = 0
            passed = False
            target = task.difficulty or 2
            while not passed:
                attempts += 1
                focus = student.skill_level + choice([0, 1, 2])
                passed = focus >= target or attempts >= 3
                mood = "success" if passed else "warn"
                log(
                    f"Exam attempt {attempts}: focus score {focus} / target {target}",
                    mood=mood,
                )
                if not passed:
                    skill_upgrade(student)
                    log(
                        f"Study sprint complete. Skill now {student.skill_level}",
                        mood="progress",
                    )
            earned += task.weight
            log(
                f"Passed {task.name}! +{task.weight * 100:.0f}% (Total {earned * 100:.1f}%)",
                mood="success",
            )

        else:  # participation
            log(
                "Show up and follow along!",
                mood="info",
            )
            earned += task.weight
            log(
                f"Participation unlocked +{task.weight * 100:.0f}% (Total {earned * 100:.1f}%)",
                mood="success",
            )

        task_index += 1

    log(
        f"Semester complete. Final simulated grade: {earned * 100:.1f}%",
        mood="progress",
    )


if __name__ == "__main__":
    main()
