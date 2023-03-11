import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource }  from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';


// Configure the open telemetry trace exporter to send traces to the backend proxy.
const exporter = new OTLPTraceExporter({
    url: `${process.env.REACT_APP_OLTP_URL}/v1/traces`,
    headers: {
      'Content-Type': 'application/json',
    },
    
});

// Configure the open telemetry web trace provider, and set the service name to `fronted-react-js`
const provider = new WebTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'fronted-react-js',
  }),
});

provider.addSpanProcessor(new BatchSpanProcessor(exporter));

provider.register({
  contextManager: new ZoneContextManager()
});
