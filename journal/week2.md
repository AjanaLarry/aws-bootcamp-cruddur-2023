# Week 2 — Distributed Tracing (Homework Challenges)

This week, I instrumented the backend flask application to use OTEL with Honeycomb as the provider. I also instrumented AWS X-Ray to observe application traces within the AWS console and installed the WatchTower to send application log data to the CloudWatch log group. Also, I completed all the Todo lists for the week. Below is a summary of the homework challenges:

# Task 1 - Instrument Honeycomb for the frontend-application

The essence of this task is to enable us to observe network latency (the duration it takes to retrieve data from the backend API) between the frontend and backend API. To achieve this, I created an additional container to act as a collector and forwarder to Honeycomb.

1. Modify the gitpod.yml file to include the required node modules as shown below:

```yaml
tasks:
    # Other Task....
    - name: npm-init
        init: |
        cd /workspace/aws-bootcamp-cruddur-2023/frontend-react-js
        npm i --save \
            @opentelemetry/api \
            @opentelemetry/sdk-trace-web \
            @opentelemetry/exporter-trace-otlp-http \
            @opentelemetry/instrumentation-document-load \
            @opentelemetry/context-zone

ports:
    # other ports...
    - port: 4318
        name: otel-collector
        visibility: public
```

2. Update the docker-compose file to include container requirements for the OTEL collector and set env keys for the frontend application:

```yaml
version: "3.8"
services:
  # Other services
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      REACT_APP_OLTP_URL: "https://4318-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}" # Opentelemetry collector service address
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
  #opentelemetry container
  otel-collector:
    image: "otel/opentelemetry-collector"
    environment:
      HONEYCOMB_API_KEY: "${HONEYCOMB_API_KEY}" # Same honeycomb API key used in the backend environment
    command: [--config=/etc/otel-collector-config.yaml]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - 14268:14268
      - 4318:4318
```

3. Create a yaml config file at the root directory to indicate the volume to be mounted for the otel-collector service:

```yaml
receivers:
  otlp:
    protocols:
      http:
        cors:
          allowed_origins:
            - https://*
            - http://*

processors:
  batch:

exporters:
  otlp:
    endpoint: "api.honeycomb.io:443"
    headers:
      "x-honeycomb-team": "${HONEYCOMB_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp]
```

4. Create a tracing.js file in the frontend/src/ directory to allow initialization of the components, as shown below:

```jsx
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource }  from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const exporter = new OTLPTraceExporter({
  url: `${process.env.REACT_APP_OLTP_URL}/v1/traces`,
  headers: {
    'Content-Type': 'application/json',
  },
  
});
const provider = new WebTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'frontend-react-js',
  }),
});
provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register({
  contextManager: new ZoneContextManager()
});
```

5. Import the file into the entry point of the react app by updating the index.js file:

```jsx
// include this line at the top of the index.js file
import './tracing.js'
```

6. Update the HomeFeedPage.js to include a custom span for measuring network latency for the homepage, as shown below:

```jsx
//Initial imports...

//Honeycomb Tracing
import { trace, context, } from '@opentelemetry/api';
const tracer = trace.getTracer();

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`
      var startTime = performance.now() //capture start time
      const res = await fetch(backend_url, {
        method: "GET"
      });
      var endTime = performance.now() //capture when result was returned

      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson)
        //Start custom span
        tracer.startActiveSpan('HomeFeedPageLoadSpan', hmfSpan => {
          // Add attributes to custom span
          hmfSpan.setAttribute('homeeFeedPage.latency_MS', (endTime - startTime)); //Latency in milliseconds
          hmfSpan.setAttribute('homeeFeedPage.status', true); //status of the item retrieved
          hmfSpan.end();
        });
      } else {
        console.log(res)
        // same as above but for when the response isn't a success
        tracer.startActiveSpan('HomeFeedPageLoadSpan', hmfSpan => {
          hmfSpan.setAttribute('homeeFeedPage.latency_MS', (endTime - startTime));
          hmfSpan.setAttribute('homeeFeedPage.status', false);
          hmfSpan.end();
        });
      }
    } catch (err) {
      console.log(err);
    }
  };

//..... The remaining code
```

7. At this point, I committed and push all updates to GitHub. Then opened a new Gitpod workspace to allow the initialization of dependencies.
8. Run docker-compose up to create our frontend, backend, and otel-collector containers. 
9. Open the frontend homepage in the browser and refresh it a couple of times to enable our span to collect sufficient data.

![HoneyComb Frontend Traces 1.png](/_docs/assets/week-2/HoneyComb_Frontend_Traces_1.png)

![HoneyComb Frontend 3.png](/_docs/assets/week-2/HoneyComb_Frontend_3.png)

![HoneyComb Frontend 2.png](/_docs/assets/week-2/HoneyComb_Frontend_2.png)

![HoneyComb Homepage latency.png](/_docs/assets/week-2/HoneyComb_Homepage_latency.png)

# Task 2 - Add a Custom Span to capture UserData

1. I modified the user_activities.py file located in the backend/services/ directory to include a custom span that captures user data activities:

```python
from datetime import datetime, timedelta, timezone
from opentelemetry import trace

tracer = trace.get_tracer("user-activities")

class UserActivities:
  def run(user_handle):
    with tracer.start_as_current_span("user-data-activities"): # start a new custom span called user-data
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
        span.set_attribute("user.now", now.isoformat() # capture the time
        span.set_attribute("UserID", user_handle) # capture the user id
        results = [{
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Andrew Brown',
          'message': 'Cloud is fun!',
          'created_at': (now - timedelta(days=1)).isoformat(),
          'expires_at': (now + timedelta(days=31)).isoformat()
        }]
        span.set_attribute("user.activities.len", len(result)) # capture the number of active user activities 
        model['data'] = results
      return model
```

2. See below the result from instrumenting the user activities:

![HoneyComb User data.png](/_docs/assets/week-2/HoneyComb_User_data.png)

This was as far as I could go with the stretch homework challenge. Thanks for the opportunity to learn.