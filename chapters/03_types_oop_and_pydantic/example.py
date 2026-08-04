"""Static contracts, runtime validation, dataclasses, and composition."""

from pydantic import ValidationError

from learn_python_quick.models import ThresholdPredictor, TrainingConfig, describe_prediction


def main() -> None:
    config = TrainingConfig(
        model_name="  Tiny MLP ",
        learning_rate=0.01,
        epochs=8,
        tags=("cpu", "tutorial"),
    )
    print(config.model_dump())

    predictor = ThresholdPredictor(threshold=0.6)
    print(describe_prediction(predictor, [0.4, 0.8, 0.9]))

    try:
        TrainingConfig(model_name="bad", learning_rate=-1, epochs=0)
    except ValidationError as error:
        fields = [item["loc"][0] for item in error.errors()]
        print(f"invalid fields={fields}")


if __name__ == "__main__":
    main()
