import datetime
import azure.functions as func

def main(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if myTimer.past_due:
        print('The timer is past due!')

    print('Pythonat %s' % utc_timestamp)

# この関数は定期的に実行されます
