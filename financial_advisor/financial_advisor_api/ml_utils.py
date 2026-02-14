import os
import tensorflow as tf
import joblib
import pandas as pd
from tensorflow.keras.layers import Layer
from groq import Groq
from django.conf import settings


# Define the custom layer (Must match your training code exactly)
class AttentionLayer(Layer):
    def build(self, input_shape):
        self.W = self.add_weight(
            name="att_weight",
            shape=(input_shape[-1], 1),
            initializer="normal",
            trainable=True,
        )
        self.b = self.add_weight(
            name="att_bias",
            shape=(input_shape[1], 1),
            initializer="zeros",
            trainable=True,
        )
        super().build(input_shape)

    def call(self, x):
        e = tf.matmul(x, self.W) + self.b
        e = tf.squeeze(e, -1)
        a = tf.nn.softmax(e)
        a = tf.expand_dims(a, -1)
        return tf.reduce_sum(x * a, axis=1)


class FinancialModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Pointing to the "saved_models" folder in root
        base_path = os.path.join(settings.BASE_DIR, "saved_models")

        self.model = tf.keras.models.load_model(
            os.path.join(base_path, "savings_model.h5"),
            custom_objects={
                "AttentionLayer": AttentionLayer,
                "mse": tf.keras.losses.MeanSquaredError(),
            },
        )
        self.scaler = joblib.load(os.path.join(base_path, "scaler.joblib"))
        self.encoder = joblib.load(os.path.join(base_path, "encoder.joblib"))
        self.categories = [
            "Groceries",
            "Transport",
            "Eating Out",
            "Entertainment",
            "Utilities",
            "Healthcare",
            "Education",
            "Misc",
        ]

    def predict(self, input_data):
        # 1. Create DataFrame
        num_df = pd.DataFrame([input_data])

        # 2. Scale Numerical Data
        # Filter only columns the scaler knows about
        num_cols = self.scaler.feature_names_in_
        num_df_scaled = num_df.copy()
        num_df_scaled[num_cols] = self.scaler.transform(num_df[num_cols])

        # 3. Encode Categorical Data
        cat_df = pd.DataFrame(
            [
                {
                    "Occupation": input_data["Occupation"],
                    "City_Tier": input_data["City_Tier"],
                }
            ]
        )
        cat_encoded = self.encoder.transform(cat_df)

        # 4. Combine
        final_input = pd.concat(
            [
                num_df_scaled[num_cols],
                pd.DataFrame(cat_encoded, columns=self.encoder.get_feature_names_out()),
            ],
            axis=1,
        )

        preds = self.model.predict(final_input, verbose=0)[0]
        return preds, self.categories


def get_groq_response(prompt):
    # Ensure you have GROQ_API_KEY in your environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "AI Insight unavailable (missing API key)."
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
