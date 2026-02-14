import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ml_utils import FinancialModel, get_groq_response


@csrf_exempt
def predict_financials(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Constants
            EXCHANGE_RATES = {"MAD": 8.35, "INR": 1.0, "USD": 83.20}
            currency = data.get("currency", "MAD")
            rate = EXCHANGE_RATES.get(currency.split()[0], 1.0)

            # Map JSON to Model Input (Normalize to base currency)
            ml_input = {
                "Income": float(data["income"]) * rate,
                "Age": int(data["age"]),
                "Dependents": 2,
                "Disposable_Income": float(data["income"]) * 0.7 * rate,
                "Desired_Savings": float(data["income"])
                * float(data["desired_savings_pct"])
                / 100
                * rate,
                "Groceries": float(data["groceries"]) * rate,
                "Transport": float(data["transport"]) * rate,
                "Eating_Out": float(data["eating_out"]) * rate,
                "Entertainment": float(data["entertainment"]) * rate,
                "Utilities": float(data["utilities"]) * rate,
                "Healthcare": 200 * rate,
                "Education": 1000 * rate,
                "Miscellaneous": float(data["misc"]) * rate,
                "Occupation": data["occupation"],
                "City_Tier": data["city_tier"],
            }

            model = FinancialModel.get_instance()
            preds_raw, categories = model.predict(ml_input)

            # Convert predictions back to user currency
            preds_user = preds_raw / rate

            # Metrics
            total_saved = float(np.sum(preds_user))
            target_goal = (
                float(data["income"]) * float(data["desired_savings_pct"]) / 100
            )

            result = {
                "total_saved": round(total_saved, 2),
                "goal_diff": round(total_saved - target_goal, 2),
                "efficiency": round((total_saved / float(data["income"])) * 100, 1),
                "top_cat": categories[int(np.argmax(preds_user))],
                "chart_labels": categories,
                "chart_data": preds_user.tolist(),
                "currency": currency,
            }

            # AI Insight
            prompt = f"Analyze: Income {data['income']}{currency}, Savings {result['total_saved']}{currency}, Top Category {result['top_cat']}. Give concise advice for a {data['occupation']}."
            result["ai_insight"] = get_groq_response(prompt)

            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)


@csrf_exempt
def chat_agent(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            user_msg = body.get("message")
            context = body.get("context", "No financial context provided.")

            prompt = f"Context: {context}. User asks: {user_msg}. Answer as a financial expert."
            response = get_groq_response(prompt)

            return JsonResponse({"response": response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "POST required"}, status=405)
