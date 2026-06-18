import pandas as pd
import os


def save_history(
    file_name,
    prediction,
    confidence
):

    history_row = pd.DataFrame([{

        "File":
        file_name,

        "Prediction":
        prediction,

        "Confidence":
        round(confidence,2)
    }])

    history_file = (
        "prediction_history.csv"
    )

    if os.path.exists(
        history_file
    ):

        history_row.to_csv(

            history_file,

            mode="a",

            header=False,

            index=False
        )

    else:

        history_row.to_csv(

            history_file,

            index=False
        )