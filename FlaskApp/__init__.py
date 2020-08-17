from flask import Flask, request, redirect, url_for, flash, render_template
from flask_login import login_required, logout_user, current_user
from flask_dance.contrib.twitter import twitter
from .config import Config
from .models import db, login_manager
from .oauth import blueprint
from .cli import create_db
import timeago
import datetime
import pytz

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
db.init_app(app)
login_manager.init_app(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("timeline"))
    return render_template('home.html')

@app.route("/timeline")
@login_required
def timeline():
    if "count" in request.args:
        timeline = blueprint.session.get('statuses/home_timeline.json', params={'count': request.args['count'], 'include_entities': 'true', 'tweet_mode': 'extended'}).json()
    else:
        timeline = blueprint.session.get('statuses/home_timeline.json', params={'count':30, 'include_entities': 'true', 'tweet_mode': 'extended'}).json()

    for tweet in timeline:
        retweet = False
        temp_tweet = tweet
        while temp_tweet["in_reply_to_status_id"] is not None:
            retweet = True
            temp_tweet = blueprint.session.get('statuses/show.json', params={'id': temp_tweet['in_reply_to_status_id']}).json()
        if retweet and temp_tweet['entities']['urls']: 
            orig_url = temp_tweet['entities']['urls'][0]['url']
            tweet['reply_orig_url'] = orig_url

        date_time_obj = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        now = datetime.datetime.now(pytz.utc)
        tweet['time_ago'] = timeago.format(date_time_obj, now)

    return render_template("home.html", messages=timeline)


if __name__ == "__main__":
    app.run()
