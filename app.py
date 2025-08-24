from flask import Flask, render_template, request

app = Flask(__name__)

# Dummy media channels for demo
MEDIA_CHANNELS = {
    "TV": {"cost_per_day": 1000, "impressions": 50000},
    "Radio": {"cost_per_day": 500, "impressions": 20000},
    "Out-of-Home": {"cost_per_day": 800, "impressions": 30000},
    "Facebook Ads": {"cost_per_day": 100, "impressions": 10000},
    "Instagram Ads": {"cost_per_day": 150, "impressions": 12000},
    "Google Ads": {"cost_per_day": 120, "impressions": 15000},
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Collect form inputs
        campaign_name = request.form.get("campaign_name")
        budget = float(request.form.get("budget"))
        target_audience = request.form.get("target_audience")
        duration = int(request.form.get("duration"))

        # Rules-based recommendations
        if budget > 5000:
            recommended_channels = ["TV", "Radio", "Out-of-Home"]
        else:
            recommended_channels = ["Facebook Ads", "Instagram Ads", "Google Ads"]

        # Calculate estimated impressions and allocated budget per channel
        recommendations = []
        per_channel_budget = budget / len(recommended_channels)
        for channel in recommended_channels:
            channel_info = MEDIA_CHANNELS[channel]
            est_impressions = int(channel_info["impressions"] * (per_channel_budget / (channel_info["cost_per_day"] * duration)))
            recommendations.append({
                "channel": channel,
                "allocated_budget": round(per_channel_budget, 2),
                "estimated_impressions": est_impressions
            })

        # Pass all data to results.html with body class
        return render_template(
            "results.html",
            body_class="results-page",
            campaign_name=campaign_name,
            budget=budget,
            target_audience=target_audience,
            duration=duration,
            recommendations=recommendations
        )

    # Pass body class for home page
    return render_template("home.html", body_class="home-page")


if __name__ == "__main__":
    app.run(debug=True)
