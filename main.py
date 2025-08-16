from dataclasses import dataclass
from enum import Enum
from random import choice, sample
import typer
from typing_extensions import Annotated


class Workout(Enum):
    PUSH = "Push"
    PULL = "Pull"
    CORE = "Core"
    LEGS = "Legs"
    YOGA = "Yoga"
    CARDIO = "Cardio"


@dataclass
class Exercise:
    desc: str
    props: list[str]

    @classmethod
    def weighted(cls, desc: str, lbs: int | None = None):
        props = ["3 sets \u00d7 10 reps"]

        if lbs is not None:
            props.append(f"{lbs} lbs")

        return cls(desc, props)


workout_exercises: dict[Workout, list[Exercise]] = {
    Workout.PUSH: [
        Exercise.weighted("Seated shoulder dumbbell presses", lbs=25),
        Exercise.weighted("Laying chest dumbbell flies", lbs=10),
        Exercise.weighted("Laying chest dumbbell presses", lbs=25),
        Exercise.weighted("Tricep body-weight dips"),
        Exercise.weighted("Inclined chest dumbbell presses", lbs=25),
        Exercise.weighted("Standing lateral dumbbell raises", lbs=10),
        Exercise.weighted("Push-ups"),
    ],
    Workout.PULL: [
        Exercise.weighted("Hanging chin-ups"),
        Exercise.weighted("Sitting lateral cable pull-downs", lbs=50),
        Exercise.weighted("Cable face pulls", lbs=25),
        Exercise.weighted("Deadlifts", lbs=50),
        Exercise.weighted("Laying dumbbell pull-overs", lbs=25),
        Exercise.weighted("Bent-over single-arm dumbbell rows", lbs=25),
        Exercise.weighted("Standing bicep curls", lbs=25),
        Exercise.weighted("Seated knee-bicep curls", lbs=25),
    ],
    Workout.CORE: [
        Exercise.weighted("Russian twists", lbs=15),
        Exercise.weighted("Sit-ups", lbs=15),
        Exercise.weighted("Oblique dumbbell crunches", lbs=40),
        Exercise.weighted("Dead bugs"),
        Exercise.weighted("Hanging knee raises"),
        Exercise.weighted("Hanging leg raises"),
        Exercise.weighted("Cable crunches", lbs=75),
        Exercise.weighted("Cable oblique twists", lbs=15),
    ],
    Workout.LEGS: [
        Exercise.weighted("Squats", lbs=50),
        Exercise.weighted("Lunges", lbs=25),
        Exercise.weighted("Leg press", lbs=100),
        Exercise.weighted("Standing calf raises", lbs=25),
        Exercise.weighted("Leg curls machine", lbs=35),
        Exercise.weighted("Leg extensions machine", lbs=35),
        Exercise.weighted("Romanian deadlifts", lbs=50),
    ],
    Workout.CARDIO: [
        Exercise("Running", ["30 min", "7mph", "*Cooldown*: 5 min"]),
        Exercise("Stair stepper", ["30 min", "Level 5", "*Cooldown*: 5 min"]),
        Exercise("Elliptical", ["30 min", "Level 5", "*Cooldown*: 5 min"]),
        Exercise("Cycling", ["30 min", "Level 5", "*Cooldown*: 5 min"]),
    ],
    # Note that Yoga has no specific exercises
}


def main(workout: Annotated[Workout, typer.Option(prompt=True, case_sensitive=False)]):
    #
    # The header
    #
    print(f"* **Target Area**: {workout.value}")
    print("")

    #
    # Cardio section
    #
    if workout != Workout.YOGA:
        match workout:
            case Workout.CARDIO:
                cardio_desc = choice(workout_exercises[Workout.CARDIO]).desc
            case Workout.PUSH | Workout.PULL:
                cardio_desc = "Running"
            case Workout.CORE:
                cardio_desc = "Elliptical"
            case Workout.LEGS:
                cardio_desc = "Stair stepper"

        # Find the matching cardio exercise to the description
        cardio_exercise = next(
            ex for ex in workout_exercises[Workout.CARDIO] if ex.desc == cardio_desc
        )

        print(f"# {cardio_exercise.desc}")
        for prop in cardio_exercise.props:
            print(f"* {prop}")
        print("")

    #
    # Strength section
    #
    if workout != Workout.YOGA and workout != Workout.CARDIO:
        print("# Strength")

        exercises = workout_exercises[workout]
        # Only sample up to 6 random exercises if there are more than 6
        if len(exercises) > 6:
            exercises = sample(exercises, 6)

        for i, exercise in enumerate(exercises, start=1):
            print(f"{i}. {exercise.desc}")

            for prop in exercise.props:
                print(f"   - {prop}")

        print("")

    #
    # Yoga section
    #
    if workout == Workout.YOGA:
        print("# Yoga")
        print("https://www.youtube.com/@yogawithadriene")
        print("")

    #
    # Stretch section
    #
    print("# Stretch")
    print("* 5 min")
    print("")


if __name__ == "__main__":
    typer.run(main)
