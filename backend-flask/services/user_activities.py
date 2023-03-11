from datetime import datetime, timedelta, timezone
from opentelemetry import trace

tracer = trace.get_tracer("user-activities")

class UserActivities:
  def run(user_handle):
    with tracer.start_as_current_span("user-data-activities"): # start a new custom spam called user-data
     span = trace.get_current_span()
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()
    span.set_attribute("user.now", now.isoformat())

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      now = datetime.now()
      span.set_attribute("user.now", now.isoformat()) # capture the time
      span.set_attribute("UserID", user_handle) # capture the user id
      results = [{
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle':  'AJLarry',
        'message': 'Thanks @andrewbrown for this empowering bootcamp!',
        'created_at': (now - timedelta(days=1)).isoformat(),
        'expires_at': (now + timedelta(days=31)).isoformat()
      }]
      span.set_attribute("user.activities.len", len(results)) # capture the number of active user activities 
      model['data'] = results
    return model