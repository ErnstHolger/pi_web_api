# Stream Updates Guide

Stream Updates is a feature in PI Web API that enables incremental data retrieval for streams without using websockets. It uses markers to track the position in a stream and efficiently retrieve only new data updates.

## Overview

Stream Updates provides:
- **Incremental updates**: Retrieve only new data since the last check
- **Marker-based tracking**: Uses markers to maintain position in the stream
- **Single or multiple streams**: Support for both individual streams and stream sets
- **Metadata change detection**: Notifies when previously received data is invalidated by metadata changes
- **No websocket required**: Uses standard HTTP requests (POST to register, GET to retrieve)

## Key Concepts

### Markers
A marker identifies a specific position in a stream. When you register for updates or retrieve updates, you receive a `LatestMarker` that represents your current position. Use this marker in subsequent requests to get only new data.

### Registration
Before retrieving updates, you must register the stream(s) you want to monitor. Registration returns:
- `LatestMarker`: Your starting position in the stream
- `Status`: Registration status (Succeeded, AlreadyRegistered, or Failed)
- Links to retrieve updates

### Retrieving Updates
Use the marker from registration (or a previous retrieval) to get new updates. Each response includes:
- `Items`: Array of new data points since the last marker
- `LatestMarker`: New marker for the next retrieval
- Links for continuous polling

## Basic Usage

### Single Stream Updates

```python
from pi_web_sdk import PIWebAPIClient
from pi_web_sdk.config import PIWebAPIConfig
import time

# Configure client
config = PIWebAPIConfig(
    base_url="https://your-pi-server/piwebapi",
    username="your-username",
    password="your-password"
)
client = PIWebAPIClient(config)

# Get stream WebID from an attribute
attr = client.attribute.get_by_path(r"\\Server\Database\Element|Attribute")
stream_web_id = attr["WebId"]

# Step 1: Register for updates
registration = client.stream.register_update(stream_web_id)
marker = registration["LatestMarker"]

# Step 2: Poll for updates
while True:
    time.sleep(5)  # Wait between polls
    
    # Retrieve updates
    updates = client.stream.retrieve_update(marker)
    
    # Process new data
    for item in updates.get("Items", []):
        timestamp = item["Timestamp"]
        value = item["Value"]
        print(f"{timestamp}: {value}")
    
    # Update marker for next iteration
    marker = updates["LatestMarker"]
```

### Multiple Streams Updates (Stream Sets)

```python
# Get multiple stream WebIDs
stream_web_ids = [
    client.attribute.get_by_path(r"\\Server\DB\Element1|Temp")["WebId"],
    client.attribute.get_by_path(r"\\Server\DB\Element2|Pressure")["WebId"],
    client.attribute.get_by_path(r"\\Server\DB\Element3|Flow")["WebId"],
]

# Register all streams
registration = client.streamset.register_updates(stream_web_ids)
marker = registration["LatestMarker"]

# Poll for updates from all streams
while True:
    time.sleep(5)
    
    updates = client.streamset.retrieve_updates(marker)
    
    # Process updates per stream
    for stream_update in updates.get("Items", []):
        stream_id = stream_update["WebId"]
        for item in stream_update.get("Items", []):
            print(f"Stream {stream_id}: {item['Timestamp']} = {item['Value']}")
    
    marker = updates["LatestMarker"]
```

## Advanced Features

### Selected Fields
Reduce response size by selecting only needed fields:

```python
# Register with selected fields
registration = client.stream.register_update(
    stream_web_id,
    selected_fields="Items.Timestamp;Items.Value"
)

# Retrieve with selected fields
updates = client.stream.retrieve_update(
    marker,
    selected_fields="Items.Value"
)
```

### Unit Conversion
Convert values to desired units during retrieval:

```python
# Get temperature in Fahrenheit
updates = client.stream.retrieve_update(
    marker,
    desired_units="degF"
)
```

### Error Handling
Stream Updates requires proper error handling for robust applications:

```python
marker = None

while True:
    try:
        # Register if needed
        if marker is None:
            registration = client.stream.register_update(stream_web_id)
            
            if registration.get("Status") == "Failed":
                exception = registration.get("Exception")
                print(f"Registration failed: {exception}")
                time.sleep(10)
                continue
            
            marker = registration["LatestMarker"]
        
        # Retrieve updates
        time.sleep(5)
        updates = client.stream.retrieve_update(marker)
        
        # Check for errors
        if "Errors" in updates:
            print(f"Errors: {updates['Errors']}")
            # Re-register on error
            marker = None
            continue
        
        # Process updates
        items = updates.get("Items", [])
        # ... process items ...
        
        marker = updates["LatestMarker"]
        
    except Exception as e:
        print(f"Exception: {e}")
        # Clear marker to force re-registration
        marker = None
        time.sleep(10)
```

## Registration Status

When registering for updates, check the status:

```python
registration = client.stream.register_update(stream_web_id)

status = registration.get("Status")
if status == "Succeeded":
    # New registration
    marker = registration["LatestMarker"]
elif status == "AlreadyRegistered":
    # Stream was already registered
    marker = registration["LatestMarker"]
elif status == "Failed":
    # Registration failed
    exception = registration.get("Exception")
    print(f"Failed: {exception}")
```

## Metadata Changes

Stream Updates detects metadata changes that invalidate previous data:
- Changing the data reference for an attribute
- Changing the unit of measure
- Deleting an attribute

When metadata changes occur:
1. An error is returned in the updates response
2. Previous data is no longer valid
3. You must re-register and fetch fresh data

```python
updates = client.stream.retrieve_update(marker)

if "Errors" in updates:
    # Metadata changed - re-register and fetch fresh data
    registration = client.stream.register_update(stream_web_id)
    marker = registration["LatestMarker"]
    
    # Fetch current data using other endpoints
    current = client.stream.get_recorded(
        stream_web_id,
        start_time="*-1d",
        end_time="*"
    )
```

## Best Practices

1. **Handle errors gracefully**: Always check for errors and re-register when needed
2. **Adjust poll interval**: Balance between data freshness and server load
3. **Use selected fields**: Reduce bandwidth by selecting only needed fields
4. **Monitor registration status**: Check if already registered to avoid duplicates
5. **Store markers**: Consider persisting markers to resume after application restart
6. **Load balancer affinity**: When using a load balancer, configure server affinity
7. **Timeout handling**: Implement timeouts for long-running connections

## API Reference

### StreamController

#### `register_update(web_id, selected_fields=None)`
Register a stream for updates.

**Parameters:**
- `web_id` (str): WebID of the stream
- `selected_fields` (str, optional): Comma-separated list of fields

**Returns:** Dictionary with `LatestMarker` and `Status`

#### `retrieve_update(marker, selected_fields=None, desired_units=None)`
Retrieve updates using a marker.

**Parameters:**
- `marker` (str): Marker from previous call
- `selected_fields` (str, optional): Fields to include
- `desired_units` (str, optional): Unit conversion

**Returns:** Dictionary with `Items` (updates) and `LatestMarker`

### StreamSetController

#### `register_updates(web_ids, selected_fields=None)`
Register multiple streams for updates.

**Parameters:**
- `web_ids` (List[str]): List of stream WebIDs
- `selected_fields` (str, optional): Fields to include

**Returns:** Dictionary with `Items` (registration per stream) and `LatestMarker`

#### `retrieve_updates(marker, selected_fields=None, desired_units=None)`
Retrieve updates for multiple streams.

**Parameters:**
- `marker` (str): Marker from previous call
- `selected_fields` (str, optional): Fields to include
- `desired_units` (str, optional): Unit conversion

**Returns:** Dictionary with `Items` (updates per stream) and `LatestMarker`

## Examples

See [stream_updates_example.py](stream_updates_example.py) for complete working examples including:
- Single stream polling
- Multiple stream polling
- Unit conversion
- Error handling patterns

## Limitations

- Markers expire after a period of inactivity (server-configured)
- Using a load balancer requires server affinity configuration
- Update actions (modifying data) are not supported through Stream Updates
- Static value changes for AF Attributes are returned as normal updates
- Metadata changes cause stream unregistration and require re-registration

## References

- [PI Web API Reference](https://docs.aveva.com/bundle/pi-web-api-reference/page/help/getting-started.html)
- [Stream Updates Documentation](https://docs.aveva.com/)
